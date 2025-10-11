from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app, flash
from datetime import datetime, timedelta
import json

manager = Blueprint('manager', __name__, template_folder='../templates')

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.transactionManager'))

@manager.route('/transactionManager', methods=['GET', 'POST'])
@login_required
def transactionManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
    
    try:
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
        
        # Get transactions with filters and pagination
        transactions, total_count, pagination = Transaction.get_transactions_with_filters(filters, page, per_page)
        
        # First try a simple template test
        try:
            return render_template('backstage.html', user=current_user.name)
        except Exception as backstage_error:
            # If backstage template fails, create inline HTML
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>交易管理系統</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js"></script>
            </head>
            <body>
                <nav class="navbar navbar-dark bg-dark">
                    <div class="container-fluid">
                        <span class="navbar-brand">台積電園區周邊房屋交易管理系統</span>
                        <span class="text-white">管理者：{current_user.name}</span>
                        <a href="{url_for('api.logout')}" class="btn btn-outline-danger">登出</a>
                    </div>
                </nav>
                <div class="container mt-4">
                    <h2>交易管理</h2>
                    <p class="text-muted">管理台積電園區周邊房屋交易記錄</p>
                    
                    <!-- Add Transaction Button -->
                    <button type="button" class="btn btn-success mb-3" data-bs-toggle="modal" data-bs-target="#addTransactionModal">
                        新增交易
                    </button>
                    
                    <!-- Quick Filters -->
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5>快速篩選 - 台積電園區</h5>
                            <button type="button" class="btn btn-outline-primary me-2" onclick="filterByArea('竹科')">竹科園區</button>
                            <button type="button" class="btn btn-outline-primary me-2" onclick="filterByArea('中科')">中科園區</button>
                            <button type="button" class="btn btn-outline-primary me-2" onclick="filterByArea('南科')">南科園區</button>
                            <button type="button" class="btn btn-outline-primary me-2" onclick="filterByArea('龍潭')">龍潭園區</button>
                        </div>
                    </div>
                    
                    <!-- Transaction Table -->
                    <div class="card">
                        <div class="card-body">
                            <h5>交易記錄列表</h5>
                            <p>共 {total_count} 筆記錄</p>
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead class="table-dark">
                                        <tr>
                                            <th>交易序號</th>
                                            <th>社區名稱</th>
                                            <th>地址</th>
                                            <th>交易日期</th>
                                            <th>建物型態</th>
                                            <th>總價（萬）</th>
                                            <th>操作</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td colspan="7" class="text-center text-muted">暫無交易記錄</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Add Transaction Modal -->
                <div class="modal fade" id="addTransactionModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">新增交易記錄</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <form method="POST" action="{url_for('manager.addTransaction')}">
                                <div class="modal-body">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">社區名稱 *</label>
                                                <input type="text" class="form-control" name="community_name" required>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">地址 *</label>
                                                <textarea class="form-control" name="address" rows="2" required></textarea>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">交易日期 *</label>
                                                <input type="date" class="form-control" name="transaction_date" required>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">建物型態 *</label>
                                                <select class="form-select" name="building_type" required>
                                                    <option value="">請選擇</option>
                                                    <option value="住宅大樓">住宅大樓</option>
                                                    <option value="華廈">華廈</option>
                                                    <option value="公寓">公寓</option>
                                                    <option value="透天厝">透天厝</option>
                                                    <option value="店面">店面</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">總價（萬元） *</label>
                                                <input type="number" class="form-control" name="total_price" step="0.1" required>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">單價（萬元/坪） *</label>
                                                <input type="number" class="form-control" name="unit_price" step="0.1" required>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">總面積（坪） *</label>
                                                <input type="number" class="form-control" name="total_area" step="0.1" required>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">主要用途 *</label>
                                                <select class="form-select" name="main_use" required>
                                                    <option value="">請選擇</option>
                                                    <option value="住家用">住家用</option>
                                                    <option value="商業用">商業用</option>
                                                    <option value="工業用">工業用</option>
                                                    <option value="其他">其他</option>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">交易標的 *</label>
                                                <select class="form-select" name="transaction_target" required>
                                                    <option value="">請選擇</option>
                                                    <option value="房地(土地+建物)">房地(土地+建物)</option>
                                                    <option value="房地(土地+建物)+車位">房地(土地+建物)+車位</option>
                                                    <option value="建物">建物</option>
                                                    <option value="土地">土地</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">建築年齡（年）</label>
                                                <input type="number" class="form-control" name="building_age" min="0">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                                    <button type="submit" class="btn btn-success">新增交易</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                
                <script>
                function filterByArea(area) {{
                    alert('篩選' + area + '園區的交易記錄');
                }}
                </script>
            </body>
            </html>
            """
            
    except Exception as e:
        # If everything fails, show basic error info
        return f"""
        <h1>交易管理系統</h1>
        <p>歡迎 {current_user.name}！</p>
        <p>系統錯誤: {str(e)}</p>
        <a href="{url_for('api.logout')}">登出</a>
        """

@manager.route('/addTransaction', methods=['POST'])
@login_required
def addTransaction():
    if current_user.role == 'user':
        return jsonify({'success': False, 'message': 'No permission'})
    
    try:
        # Generate transaction ID
        transaction_id = generate_transaction_id()
        
        # Get form data
        transaction_data = {
            'id': transaction_id,
            'community_name': request.form.get('community_name'),
            'address': request.form.get('address'),
            'transaction_date': request.form.get('transaction_date'),
            'building_type': request.form.get('building_type'),
            'building_age': request.form.get('building_age'),
            'total_price': request.form.get('total_price'),
            'unit_price': request.form.get('unit_price'),
            'total_area': request.form.get('total_area'),
            'main_use': request.form.get('main_use'),
            'transaction_target': request.form.get('transaction_target'),
            'main_area_ratio': request.form.get('main_area_ratio'),
            'floor': request.form.get('floor'),
            'total_floors': request.form.get('total_floors'),
            'parking_spaces': request.form.get('parking_spaces', 0),
            'created_by': current_user.name,
            'is_hidden': False
        }
        
        # Add transaction to database
        Transaction.add_transaction(transaction_data)
        flash('交易記錄新增成功')
        
    except Exception as e:
        flash(f'新增失敗: {str(e)}')
    
    return redirect(url_for('manager.transactionManager'))

@manager.route('/transaction/<int:transaction_id>/edit')
@login_required
def getTransactionForEdit(transaction_id):
    if current_user.role == 'user':
        return jsonify({'success': False, 'message': 'No permission'})
    
    try:
        transaction = Transaction.get_transaction(transaction_id)
        if not transaction:
            return jsonify({'success': False, 'message': 'Transaction not found'})
        
        # Return the edit form HTML
        edit_html = render_template('edit_transaction_form.html', transaction=transaction)
        return jsonify({'success': True, 'html': edit_html})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@manager.route('/updateTransaction', methods=['POST'])
@login_required
def updateTransaction():
    if current_user.role == 'user':
        flash('No permission')
        return redirect(url_for('index'))
    
    try:
        transaction_id = request.form.get('transaction_id')
        
        # Get original data for history tracking
        original = Transaction.get_transaction(transaction_id)
        
        # Get updated data
        updated_data = {
            'community_name': request.form.get('community_name'),
            'address': request.form.get('address'),
            'transaction_date': request.form.get('transaction_date'),
            'building_type': request.form.get('building_type'),
            'building_age': request.form.get('building_age'),
            'total_price': request.form.get('total_price'),
            'unit_price': request.form.get('unit_price'),
            'total_area': request.form.get('total_area'),
            'main_use': request.form.get('main_use'),
            'transaction_target': request.form.get('transaction_target'),
            'main_area_ratio': request.form.get('main_area_ratio'),
            'floor': request.form.get('floor'),
            'total_floors': request.form.get('total_floors'),
            'parking_spaces': request.form.get('parking_spaces', 0),
            'modified_by': current_user.name
        }
        
        # Update transaction
        Transaction.update_transaction(transaction_id, updated_data)
        
        # Track changes for history
        changes = track_changes(original, updated_data)
        if changes:
            Transaction.add_history(transaction_id, current_user.name, changes)
        
        flash('交易記錄更新成功')
        
    except Exception as e:
        flash(f'更新失敗: {str(e)}')
    
    return redirect(url_for('manager.transactionManager'))

@manager.route('/transaction/<int:transaction_id>/view')
@login_required
def viewTransaction(transaction_id):
    try:
        transaction = Transaction.get_transaction(transaction_id)
        if not transaction:
            return jsonify({'success': False, 'message': 'Transaction not found'})
        
        # Return the view HTML
        view_html = render_template('view_transaction.html', transaction=transaction)
        return jsonify({'success': True, 'html': view_html})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@manager.route('/transaction/<int:transaction_id>/hide', methods=['POST'])
@login_required
def hideTransaction(transaction_id):
    if current_user.role == 'user':
        return jsonify({'success': False, 'message': 'No permission'})
    
    try:
        Transaction.hide_transaction(transaction_id)
        Transaction.add_history(transaction_id, current_user.name, '記錄已隱藏')
        return jsonify({'success': True, 'message': '交易記錄已隱藏'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@manager.route('/transaction/<int:transaction_id>/show', methods=['POST'])
@login_required
def showTransaction(transaction_id):
    if current_user.role == 'user':
        return jsonify({'success': False, 'message': 'No permission'})
    
    try:
        Transaction.show_transaction(transaction_id)
        Transaction.add_history(transaction_id, current_user.name, '記錄已恢復顯示')
        return jsonify({'success': True, 'message': '交易記錄已恢復顯示'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Legacy routes for backward compatibility (can be removed later)
@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    # Redirect to transaction manager
    return redirect(url_for('manager.transactionManager'))

@manager.route('/orderManager', methods=['GET', 'POST'])  
@login_required
def orderManager():
    # Redirect to transaction manager
    return redirect(url_for('manager.transactionManager'))

def generate_transaction_id():
    """Generate a unique transaction ID"""
    while True:
        # Generate ID with timestamp + random number
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_num = str(random.randrange(1000, 9999))
        transaction_id = int(timestamp + random_num)
        
        # Check if ID already exists
        if not Transaction.get_transaction(transaction_id):
            return transaction_id

def track_changes(original, updated):
    """Track changes between original and updated data"""
    changes = []
    field_names = {
        'community_name': '社區名稱',
        'address': '地址', 
        'transaction_date': '交易日期',
        'building_type': '建物型態',
        'building_age': '建築年齡',
        'total_price': '總價',
        'unit_price': '單價',
        'total_area': '總面積',
        'main_use': '主要用途',
        'transaction_target': '交易標的',
        'main_area_ratio': '主建物面積比例',
        'floor': '樓層',
        'total_floors': '總樓層數',
        'parking_spaces': '車位個數'
    }
    
    for field, chinese_name in field_names.items():
        if hasattr(original, field):
            old_value = getattr(original, field)
            new_value = updated.get(field)
            
            if str(old_value) != str(new_value):
                changes.append(f'{chinese_name}: {old_value} → {new_value}')
    
    return '; '.join(changes)
