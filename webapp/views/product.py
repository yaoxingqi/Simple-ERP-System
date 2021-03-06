# -*- coding: UTF-8 -*-
import json
from flask import render_template, request
from webapp import app
from auth.login_required import login_required
from auth.permission_required import permission_required
from db.db_product import products

__author_name__ = 'sonnyhcl'


@app.route('/product', methods=['GET'])
@login_required
def product():
    return render_template('product.html')


@app.route('/product/table', methods=['POST'])
@login_required
def get_all_products_detail():
    ret = {"data": [], "status": 'Success', "msg": ""}
    status, info = products.get_all()
    if status == "Success":
        _ = [ret['data'].append(
            {'p_id': i[0], 'p_name': i[1], "p_author_name": i[2],
             "i_id": i[3], "i_name": i[4], "i_unit_price": i[5],
             "i_ref_time": i[6], "i_note": i[7]}) for i in info]
    else:
        ret['msg'] = str(info)

    return json.dumps(ret, ensure_ascii=False)


@app.route('/product/add', methods=['POST'])
@permission_required('root')
@login_required
def add_product():
    """
    添加一个产品，同时添加该产品的第一个工艺
    这里需要更新两个表
    :return: {"status": "Success", "msg":"error_msg"}
    """
    ret = {}
    p_name = request.form.get('p_name')
    p_author = request.form.get('p_author')
    i_name = request.form.get('i_name')
    i_unit_price = request.form.get('i_unit_price')
    i_ref_time = request.form.get('i_ref_time')
    i_note = request.form.get('i_note')
    ret["status"], ret['msg'] = \
        products.add_product(p_name, i_name, i_unit_price,
                             i_ref_time, i_note, p_author)

    return json.dumps(ret, ensure_ascii=False)


@app.route('/product/add_item', methods=['POST'])
@permission_required('root')
@login_required
def add_item_for_product():
    """
    给指定某个产品添加一个工艺
    :return: 
    """
    ret = {}
    p_id = request.form.get('p_id')
    i_name = request.form.get('i_name')
    i_unit_price = request.form.get('i_unit_price')
    i_ref_time = request.form.get('i_ref_time')
    i_note = request.form.get('i_note')
    ret['status'], ret['msg'] = \
        products.add_item_for_product(i_name, i_unit_price,
                                      i_ref_time, i_note, p_id)

    return json.dumps(ret, ensure_ascii=False)


@app.route('/product/delete_item', methods=['POST'])
@permission_required('root')
@login_required
def delete_item_for_product():
    """
    删除指定产品中的某一项工艺
    如果该产品只有最后一个工艺，则返回错误信息
    删除最后一个工艺这个操作应该在删除产品中来做
    :return: 
    """
    ret = {}
    p_id = request.form.get('p_id')
    i_id = request.form.get('i_id')
    ret['status'], ret['msg'] = products.delete_item_for_product(p_id, i_id)

    return json.dumps(ret, ensure_ascii=False)


@app.route('/product/modify', methods=['POST'])
@permission_required('root')
@login_required
def modify_product_and_its_one_item():
    """
    每次修改只针对一个产品和它的一个工艺
    :return: {"status": "Success", "msg":"error_msg"}
    """
    ret = {}
    p_id = request.form.get('p_id')
    p_name = request.form.get('p_name')
    p_author = request.form.get('p_author')
    i_id = request.form.get('i_id')
    i_name = request.form.get('i_name')
    i_unit_price = request.form.get('i_unit_price')
    i_ref_time = request.form.get('i_ref_time')
    i_note = request.form.get('i_note')
    ret["status"], ret['msg'] = \
        products.update_product(p_id, i_id, p_name, p_author,
                                i_name, i_unit_price, i_ref_time, i_note)

    return json.dumps(ret, ensure_ascii=False)


@app.route('/product/delete', methods=['POST'])
@permission_required('root')
@login_required
def delete_product():
    """
    删除这个产品，以及这个产品的所有工艺
    :return: {"status": "Success", "msg":"error_msg"}
    """
    ret = {}
    p_id = request.form.get('p_id')
    ret["status"], ret["msg"] = products.delete_product(p_id)

    return json.dumps(ret, ensure_ascii=False)
