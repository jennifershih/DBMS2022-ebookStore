import re, math, random, string
from typing_extensions import Self
from flask import Flask, request, render_template, template_rendered, Blueprint, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
from sqlalchemy import null
from link import *
from api.sql import Member, Order_List, Product, Shopping_Detail, Cart, Transaction

store = Blueprint('user', __name__, template_folder='../templates')

@store.route('/', methods=['GET', 'POST'])
@login_required
def transaction():
    if request.method == 'GET':
        if(current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('index'))

    # Simple product listing without search
    book_row = Product.get_all_product()
    book_data = []
    for i in book_row:
        pid = i[0]
        pname = i[1]
        price = i[2]
        pic = i[5]
        
        book = {
            '商品編號': pid,
            '商品名稱': pname,
            '商品價格': price,
            '商品圖片': pic
        }
        book_data.append(book)
    
    return render_template('transaction.html', book_data=book_data, user=current_user.name)

# 會員購物車
@store.route('/cart', methods=['GET', 'POST'])
@login_required # 使用者登入後才可以看
def cart():

    # 以防管理者誤闖
    if request.method == 'GET':
        if( current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('index'))

    # 回傳有 pid 代表要 加商品
    if request.method == 'POST':
        
        if "pid" in request.form :
            data = Cart.get_cart(current_user.id)
            
            if(data == None): #假如購物車裡面沒有他的資料
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                input = { 
                    'aidd': 1, 
                    'time': time
                }
                Cart.add_cart(input) # 幫他加一台購物車
                data = Cart.get_cart(current_user.id) 
                
            tno = data[2] # 取得交易編號
            pid = request.values.get('pid') # 使用者想要購買的東西
            # 檢查購物車裡面有沒有商品
            input = (pid, tno)
            
            product = Shopping_Detail.check_product(input)
            # 取得商品價錢
            price = Product.get_product(pid)[2]

            # 如果購物車裡面沒有的話 把他加一個進去
            if(product == None):
                Shopping_Detail.add_product( {'id': tno, 'tno':pid, 'price':price, 'total':price} )
            else:
                # 假如購物車裡面有的話，就多加一個進去
                input = (tno, pid)
                amount = Shopping_Detail.get_amount(input)
                total = (amount+1) * int(price)
                Shopping_Detail.update_product({'amount':amount+1, 'tno':tno , 'pid':pid, 'total':total})

        elif "delete" in request.form :
            pid = request.values.get('delete')
            tno = Cart.get_cart(current_user.id)[2]
            input = (tno, pid)
            Member.delete_product(input)
            product_data = only_cart()
        
        elif "user_edit" in request.form:
            change_order()  
            return redirect(url_for('user.transaction'))
        
        elif "buy" in request.form:
            change_order()
            return redirect(url_for('user.order'))

        elif "order" in request.form:
            tno = Cart.get_cart(current_user.id)[2]
            total = Shopping_Detail.get_total_money(tno)
            Cart.clear_cart(current_user.id)

            time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            input = (current_user.id, time, total, tno)
            Order_List.add_order(input)

            return render_template('complete.html', user=current_user.name)

    product_data = only_cart()
    
    if product_data == 0:
        return render_template('empty.html', user=current_user.name)
    else:
        return render_template('cart.html', data=product_data, user=current_user.name)

@store.route('/order')
def order():
    data = Cart.get_cart(current_user.id)
    tno = data[2]

    product_row = Shopping_Detail.get_shopping_detail(tno)
    product_data = []

    for i in product_row:
        pname = Product.get_name(i[1])
        product = {
            '商品編號': i[1],
            '商品名稱': pname,
            '商品價格': i[3],
            '數量': i[2]
        }
        product_data.append(product)
    
    total = Shopping_Detail.get_total(tno)[0]

    return render_template('order.html', data=product_data, total=total, user=current_user.name)

@store.route('/orderlist')
def orderlist():
    if "oid" in request.args :
        pass
    
    user_id = current_user.id

    data = Member.get_order(user_id)
    orderlist = []

    for i in data:
        temp = {
            '訂單編號': i[0],
            '訂單總價': i[3],
            '訂單時間': i[2]
        }
        orderlist.append(temp)
    
    orderdetail_row = Order_List.get_orderdetail()
    orderdetail = []

    for j in orderdetail_row:
        temp = {
            '訂單編號': j[0],
            '商品名稱': j[1],
            '商品單價': j[2],
            '訂購數量': j[3]
        }
        orderdetail.append(temp)


    return render_template('orderlist.html', data=orderlist, detail=orderdetail, user=current_user.name)

def change_order():
    data = Cart.get_cart(current_user.id)
    tno = data[2] # 使用者有購物車了，購物車的交易編號是什麼
    product_row = Shopping_Detail.get_shopping_detail(data[2])

    for i in product_row:
        
        # i[0]：交易編號 / i[1]：商品編號 / i[2]：數量 / i[3]：價格
        if int(request.form[i[1]]) != i[2]:
            Shopping_Detail.update_product({
                'amount':request.form[i[1]],
                'pid':i[1],
                'tno':tno,
                'total':int(request.form[i[1]])*int(i[3])
            })
            print('change')

    return 0


def only_cart():
    
    count = Cart.check(current_user.id)

    if(count == None):
        return 0
    
    data = Cart.get_cart(current_user.id)
    tno = data[2]
    product_row = Shopping_Detail.get_shopping_detail(tno)
    product_data = []

    for i in product_row:
        pid = i[1]
        pname = Product.get_name(i[1])
        price = i[3]
        amount = i[2]
        
        product = {
            '商品編號': pid,
            '商品名稱': pname,
            '商品價格': price,
            '數量': amount
        }
        product_data.append(product)
    
    return product_data

@store.route('/userSearch', methods=['GET', 'POST'])
@login_required
def userSearch():
    # Only allow non-manager users to access this
    if current_user.role == 'manager':
        flash('管理者請使用後台管理功能')
        return redirect(url_for('manager.transactionManager'))
    
    # Get filter parameters from request
    filters = {
        'community': request.args.get('community', ''),
        'address': request.args.get('address', ''),
        'date_start': request.args.get('date_start', ''),
        'date_end': request.args.get('date_end', ''),
        'building_type': request.args.get('building_type', ''),
        'age_min': request.args.get('age_min', ''),
        'age_max': request.args.get('age_max', ''),
        'price_min': request.args.get('price_min', ''),
        'price_max': request.args.get('price_max', ''),
        'unit_price_min': request.args.get('unit_price_min', ''),
        'unit_price_max': request.args.get('unit_price_max', ''),
        'area_min': request.args.get('area_min', ''),
        'area_max': request.args.get('area_max', ''),
        'main_use': request.args.get('main_use', ''),
        'transaction_target': request.args.get('transaction_target', ''),
        'main_area_ratio_min': request.args.get('main_area_ratio_min', ''),
        'main_area_ratio_max': request.args.get('main_area_ratio_max', ''),
        'floor_min': request.args.get('floor_min', ''),
        'floor_max': request.args.get('floor_max', ''),
        'total_floors_min': request.args.get('total_floors_min', ''),
        'total_floors_max': request.args.get('total_floors_max', ''),
    }
    
    # Get page number for pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    transactions = []
    total_count = 0
    pagination = None
    summary_stats = None
    
    # Only search if at least one filter is provided
    if any(filters.values()):
        try:
            # Get visible transactions only for user search
            transactions, total_count, pagination = Transaction.get_visible_transactions_with_filters(filters, page, per_page)
            
            # Calculate summary statistics
            if transactions:
                summary_stats = Transaction.get_summary_statistics(filters)
        except Exception as e:
            flash(f'搜尋時發生錯誤: {str(e)}')
    
    return render_template('userSearch.html', 
                         transactions=transactions, 
                         total_count=total_count,
                         pagination=pagination,
                         summary_stats=summary_stats,
                         user=current_user.name)
