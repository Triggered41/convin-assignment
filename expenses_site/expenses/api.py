from django.contrib.auth.hashers import make_password, check_password, verify_password
from django.http import HttpResponse, HttpRequest, FileResponse
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from django.db.models import Sum
from expenses.models import UserModel, UserForm, ExpenseModel
import json
import logging
from fpdf import FPDF


def create_user(request: HttpRequest):
    if request.method != "POST": return HttpRequest()

    try:
        new_user = UserForm(request.POST.dict())
        if new_user.is_valid():
            transaction = new_user.save(commit=False)
            transaction.password = make_password(new_user.cleaned_data['password'])
            transaction.status = 1
            transaction.save()
            return redirect('/login')
        return HttpResponse("Failed")
    except:
        return HttpResponse("Invalid data")

def get_user(request: HttpRequest):
    if request.method != "GET": return HttpRequest()
    if not request.session.get('user_info', False): return HttpResponse("User not logged in")

    try:
        user = UserModel.objects.get(email=request.session.get('user_info')['email'])
        d = model_to_dict(user)
        del d['password']
        user_json = json.dumps(d)
        return HttpResponse(user_json, content_type="application/json")
    except:
        return HttpResponse('{"Error": "Error"}', content_type="application/json")

def user_login(request: HttpRequest):
    if request.method != 'POST': return HttpResponse()
    try:
        data = request.POST
        mail = data.get('email')
        user = UserModel.objects.get(email=mail)
        check = check_password(data['password'], user.password)
        user.password = ''
        assert(check)
        request.session['user_info'] = model_to_dict(user)
        return redirect('/')
    except:
        return HttpResponse("User not found")

def add_expense(request: HttpRequest):
    if request.method != 'POST': return HttpResponse("Wrong method")
    if not request.session.get('user_info', False): return HttpResponse("User not logged in")
    try:
        data = request.POST.dict()
        user = UserModel.objects.get(id=request.session.get('user_info', {})['id'])
        exp = ExpenseModel.objects.create(user=user, detail=data['details'], expense=data['expense'])
        exp.save()
        return redirect('/')
    except:
        return HttpResponse("Could not add expense")

def get_user_expenses(request: HttpRequest, mail: str):
    if request.method != 'GET': return HttpResponse('Wrong method')

    try:
        user = UserModel.objects.get(email=mail)
        expenses = ExpenseModel.objects.filter(user_id=user.id).values()
        return HttpResponse(json.dumps([expense for expense in expenses]), content_type="application/json")
    except:
        return HttpResponse('{"Error": "Error in retrieving expenses"}', content_type="application/json")

def get_all_expenses(request: HttpRequest):
    if request.method != 'GET': return HttpResponse('Wrong method')

    try:
        expenses = ExpenseModel.objects.all().values()
        return HttpResponse(json.dumps([expense for expense in expenses]), content_type="application/json")
    except:
        return HttpResponse("Error in retrieving expenses")

def get_overall_expense(request: HttpRequest):
    if request.method != 'GET': return HttpResponse('Wrong method')

    try:
        total = ExpenseModel.objects.aggregate(Sum('expense'))
        return HttpResponse(json.dumps(total), content_type="application/json")
    except:
        return HttpResponse("Can't find overall expenses")

def get_balance_sheet(request: HttpRequest):
    if request.method != 'GET': return HttpResponse("Wrong method")

    try:
        expenses = ExpenseModel.objects.raw('select * from expenses_usermodel join expenses_expensemodel on expenses_usermodel.id=expenses_expensemodel.user_id order by expenses_expensemodel.user_id')
        expenses_dict = {}
        for expense in expenses:
            if expense.user_id not in expenses_dict:
                expenses_dict[expense.user_id] = []
            exp_dict = model_to_dict(expense)
            exp_dict['user'] = model_to_dict(expense.user)
            del exp_dict['user']['password']
            expenses_dict[expense.user_id].append(exp_dict)
        buffer = to_pdf(expenses_dict)
        return FileResponse(open('./check.pdf', 'rb'), as_attachment=True)
        # return HttpResponse('DONE')
    except:
        return HttpResponse('NOO')

def to_pdf(data: dict):
    final_str = ''
    grand_total = 0

    for user in data:
        expenses = data[user]
        for exp in expenses:
            grand_total += exp['expense']

    for user in data:
        expenses = data[user]
        total = 0
        
        if len(expenses)>0: final_str += f'\nName: {expenses[0]['user']['name']}\n\n{'Detail':<15}Price\n\n'
        for exp in expenses:
            # final_str += f'{exp['detail']+': ':<15}{str(exp['expense'])}\n'
            final_str += f"{exp['detail']:<15}{exp['expense']}\n"
            total += exp['expense']
        final_str += '______________________\n'
        final_str += f'{'Exact Split ':<15}{total}\n'
        final_str += f'{'Equal Split ':<15}{grand_total/len(data):.2f}\n'
        final_str += f'{'Percent Split ':<15}{(total/grand_total)*100:.2f}%\n'
    final_str += f'\ntotal expense = {grand_total}'
    
    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.set_font('Courier', size=15)
        for line in final_str.split('\n'):
            pdf.cell(50, 7, txt=line, ln=1, align='L')
        pdf.output('./check.pdf')
        return pdf.buffer
    except:
        logging.exception('Msg: ')

# def get_all_expenses(request: HttpRequest):
#     if request.method != 'GET': return HttpResponse('Wrong method')

#     try:
#         expenses = ExpenseModel.objects.raw('select * from expenses_usermodel join expenses_expensemodel on expenses_usermodel.id=expenses_expensemodel.user_id')
#         expenses_list = []
#         for expense in expenses:
#             exp_dict = model_to_dict(expense)
#             exp_dict['user'] = model_to_dict(expense.user)
#             del exp_dict['user']['password']
#             expenses_list.append(exp_dict)
#         return HttpResponse(json.dumps(expenses_list), content_type="application/json")
#     except:
#         return HttpResponse("Error in retrieving expenses")
