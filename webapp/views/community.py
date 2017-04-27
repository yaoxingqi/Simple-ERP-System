# -*- coding: UTF-8 -*-
"""
社区页面的路由操作
"""
import json
from flask import render_template, session, request
from webapp import app
from db.db_community import *
from auth.login_required import login_required

__author__ = 'sonnyhcl'


@app.route('/community', methods=['GET'])
@login_required
def community_index():
    return render_template('community.html')


@app.route('/community/table/<int:c_id>', methods=['POST'])
@login_required
def get_community_by_cid(c_id):
    """
    根据c_id返回社区的信息
    c_id=0意味着返回所有社区的信息，否则只返回该c_id社区的信息。
    :param c_id: 
    :return: {"data": [{'c_id':,'c_name':,'u_name':,'u_phone':,'u_id':}], 
                "status": status, "msg":""}
    """
    status, info = community.get_community_by_cid(c_id)
    ret = {"data": [], "status": status, "msg": ""}
    if status == "Success":
        _ = [ret['data'].append({'c_id': i[0], 'c_name': i[1], 'u_id': i[4],
                                 'u_name': i[2], 'u_phone': i[3]}) for i in
             info]
    else:
        ret['msg'] = info
    return json.dumps(ret, ensure_ascii=False)


@app.route('/community/get_all_admin', methods=['POST'])
@login_required
def get_all_admin():
    """
    返回所有权限为admin & root的人的信息
    :return: {"data": [{'u_id':, 'u_name':}], 
                "status": status, "msg":""}
    """
    # TODO 返回所有admin以及root权限的人的{u_id, u_name}
    # status, response = community.get_all_admin()
    response = {'data': [{'u_id': 0, 'u_name': 'hcl'},
                         {'u_id': 1, 'u_name': 'admin'}],
                'status': 'Success', 'msg': "error_msg"}
    return json.dumps(response, ensure_ascii=False)


@app.route('/community/add', methods=['POST'])
@login_required
def add_community():
    """
    根据传入的{c_name, u_id}添加一个社区信息
    :return: {"status": "Success", "msg":"error_msg"}
    """
    c_name = request.form.get('c_name')
    u_id = request.form.get('u_id')
    # TODO 修改返回格式和传入参数
    # status, msg = community.add_community(c_name, u_id)
    status = community.add_community(c_name, u_id)
    return json.dumps({"status": status, "msg": "error_msg"})


@app.route('/community/modify', methods=['POST'])
@login_required
def modify_community():
    """
    根据传入的{c_name, c_id, u_id}修改一个社区信息
    :return: {"status": "Success", "msg":"error_msg"}
    """
    c_name = request.form.get('c_name')
    c_id = request.form.get('c_id')
    u_id = request.form.get('u_id')
    # TODO 修改返回格式
    # status， msg = community.update_community(c_id, c_name, u_id)
    status = community.update_community(c_id, c_name, u_id)
    return json.dumps({"status": status, "msg": "error_msg"})


@app.route('/community/delete', methods=['POST'])
@login_required
def delete_community():
    """
    根据传入的{c_id}删除一个社区信息
    :return: {"status": "Success", "msg":"error_msg"}
    """
    c_id = request.form.get('c_id')
    # TODO 只能删除没有人的社区以及没有订单的社区，也就是刚刚新建什么操作都没有做的社区
    # 订单的操作可以等开始做订单页面了再搞
    status = community.delete_community(c_id)
    return json.dumps({"status": status, "msg": "error_msg"})
