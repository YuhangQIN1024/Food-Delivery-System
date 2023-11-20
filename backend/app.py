import datetime
import json
import random

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

import auth
from aliyunsms.sms_send import send_sms
from config import BaseConfig

# 创建redis对象
redis_store = StrictRedis(host=BaseConfig.REDIS_HOST, port=BaseConfig.REDIS_PORT, decode_responses=True)

# 跨域
from flask_cors import cross_origin

app = Flask(__name__)

# 添加配置数据库
app.config.from_object(BaseConfig)
# 初始化拓展,app到数据库的ORM映射
db = SQLAlchemy(app)

# 检查数据库连接是否成功
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute("select 1")
        print(rs.fetchone())
        print("数据库连接成功")


# 用户登录
@app.route("/api/user/login", methods=["POST"])
@cross_origin()
def user_login():
    print("0")
    print(request.json)
    print("1")
    userortel = request.json.get("userortel").strip()
    password = request.json.get("password").strip()
    sql = ('select * ' \
           + 'from user ' \
           + 'where telephone = "{0}" and password = "{1}"').format(userortel, password)
    data = db.session.execute(sql).first()
    print(data)
    if data != None:
        user = {'id': data[0], 'password': data[1], 'telephone': data[2]}
        # 生成token
        token = auth.encode_func(user)
        print(token)
        return jsonify({"code": 200, "msg": "登录成功", "token": token})
    else:
        return jsonify({"code": 1000, "msg": "用户名或密码错误"})

@app.route("/api/user/login_manager", methods=["POST"])
@cross_origin()
def user_login_manager():
    print("0")
    print(request.json)
    print("1")
    userortel = request.json.get("userortel").strip()
    password = request.json.get("password").strip()
    sql = ('select * ' \
           + 'from manager ' \
           + 'where telephone = "{0}" and password = "{1}"').format(userortel, password)
    data = db.session.execute(sql).first()
    print(data)
    if data != None:
        manager = {'id': data[0], 'password': data[1], 'telephone': data[2]}
        # 生成token
        token = auth.encode_func(manager)
        print(token)
        return jsonify({"code": 200, "msg": "登录成功", "token": token})
    else:
        return jsonify({"code": 1000, "msg": "用户名或密码错误"})

# 用户注册__发送验证码
@app.route("/api/user/register/send_sms", methods=["POST"])
@cross_origin()
def register_sms():
    print(request.json)
    phone = request.json.get("telephone")
    print(str(phone))
    # 生成随机的6位验证码
    num = random.randrange(100000, 999999)
    params = {'code': 123456}
    params['code'] = num

    # 将验证码保存到redis中，第一个参数是key，第二个参数是value，第三个参数表示60秒后过期
    redis_store.set('valid_code:{}'.format(phone), num, 80)
    print(redis_store.get('valid_code:{}'.format(phone)))
    # 调用send_sms函数来发送短信验证码
    result = send_sms(str(phone), json.dumps(params))
    print(result)
    if result[3]:
        return jsonify({"code": "200", "msg": "验证码发送成功"})
    else:
        return jsonify({"code": '1000', "msg": "验证码发送失败"})


# 用户注册__检测验证码和手机是否在数据库中
@app.route("/api/user/register/test", methods=["POST"])
@cross_origin()
def register_test():
    rq = request.json
    # 获取验证码和手机号
    password = rq.get("password")
    vercode = rq.get("vercode")
    telephone = rq.get("telephone")

    # 先判断验证码对错
    print("this" + vercode + telephone)
    print(redis_store.get('valid_code:{}'.format(telephone)))
    if vercode != redis_store.get('valid_code:{}'.format(telephone)):
        return jsonify({"status": "1000", "msg": "验证码错误"})

    data = db.session.execute('select * from user where telephone="%s"' % telephone).fetchall()
    if not data:
        db.session.execute('insert into user(password,telephone) value("%s","%s")' % (
            password, telephone))
        db.session.commit()
        return jsonify({"status": "200", "msg": "注册成功"})
    else:
        return jsonify({"status": "1000", "msg": "该用户已存在"})


# 用户界面获取店铺信息
@app.route("/api/user/shop", methods=["GET"])
@cross_origin()
def user_get_shop():
    data = db.session.execute('select * from fastfood_shop').fetchall()

    Data = []
    for i in range(len(data)):
        dic = dict(shop_name=data[i][0], price=data[i][1], sale=data[i][2])
        Data.append(dic)
    print(Data)
    return jsonify(status=200, tabledata=Data)


# 下订单
@app.route("/api/user/addorder", methods=["POST"])
@cross_origin()
def user_addorder():
    rq = request.json
    # 获取各个参数
    phone = get_token_phone(request.headers.get('token'))
    data = db.session.execute('select * from user where telephone="%s"' % phone).fetchall()
    userid=data[0][0]
    shopname = rq.get("shop_name")
    ordermoney = rq.get("order_money")
    consphone = phone
    consname = rq.get("cons_name")
    consaddre = rq.get("cons_addre")
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_way= rq.get("order_way")
    print(shopname, ordermoney, order_way, consphone, consname, consaddre)
    db.session.execute(
        'insert into oorder( shop_name, order_money, cons_phone, cons_name, cons_addre,create_time,order_way) value("%s", %d, "%s", "%s", "%s","%s","%s")' % (
            shopname, ordermoney,  consphone, consname, consaddre, create_time,order_way))
    db.session.commit()
    print(1)
    data=db.session.execute(
        'select * from oorder where  create_time="%s"' %(create_time)
    ).fetchall()
    data01=data[0][0]
    print(data01)
    db.session.execute('insert into buy(user_id,order_id) value(%d,"%d")' % (userid,data01))
    db.session.commit()
    return jsonify(status=200, msg="成功下单")


def get_token_phone(token):
    data = auth.decode_func(token)
    phone = data['telephone']
    return (phone)


@app.route("/api/user/expensive", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_expensive():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))

        data = db.session.execute('select * from expensive_order where cons_phone="%s"' % phone).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
                       cons_phone=data[i][4],
                       cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8],
                       disp_phone=data[i][9])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/user/cheap", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_cheap():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute('select * from cheap_order where cons_phone="%s"' % phone).fetchall()
        Data = []
        print(Data)
        print("cheap")
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
                       cons_phone=data[i][4],
                       cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8],
                       disp_phone=data[i][9])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/user/usermsg", methods=["POST", "GET"])
@cross_origin()
def usermsg():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        print(phone)
        data = db.session.execute('select * from user_msg where phone="%s"' % phone).fetchall()
        print(data)
        Data = dict(user_ID=data[0][0],real_name=data[0][1], sex=data[0][2], age=data[0][3], mail=data[0][4], phone=data[0][5],
                    user_name=data[0][6])


        return jsonify(status=200, data=Data)


@app.route("/api/user/usertest", methods=["POST", "GET"])
@cross_origin()
def usertest():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute('select * from user where telephone="%s"' % phone).fetchall()
        Data = dict(user_ID=data[0][0])

        return jsonify(status=200, data=Data)


@app.route("/api/user/usermsg_chg", methods=["POST"])
@cross_origin()
def usermsg_chg():
    if request.method == 'POST':
        new_id = request.json.get('new_user_id')
        new_real_name = request.json.get('new_real_name')
        new_sex = request.json.get('new_sex')
        new_age = request.json.get('new_age')
        new_mail = request.json.get('new_mail')
        new_phone = request.json.get('new_phone')
        new_user_name = request.json.get('new_user_name')
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute('select * from user_msg where id!="%s" and phone="%s"' % (new_id,new_phone)).fetchall()
        print(data)
        if not data:
            db.session.execute(

                'insert into user_msg(id,real_name,sex,age,mail,phone,user_name) value("%s","%s", "%s", "%s", "%s", "%s","%s")' % (
                    new_id, new_real_name, new_sex, new_age, new_mail, new_phone, new_user_name))
            db.session.commit()
            return jsonify(status=200, msg="成功修改")
        else:
            return jsonify(status=1000, msg="号码已存在")


@app.route("/api/user/pwd_chg", methods=["POST"])
@cross_origin()
def user_pwd_chg():
    if request.method == 'POST':
        pwd = request.json.get('new_pwd')
        old_pwd = request.json.get('old_pwd')
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute(
            'select * from user where telephone="%s" and password="%s"' % (phone, old_pwd)).fetchall()
        if not data:
            return jsonify(status=1000, msg="原始密码错误")
        else:
            db.session.execute('update user set password="%s" where telephone="%s"' % (pwd, phone))
            db.session.commit()
            return jsonify(status=200, msg="修改成功")


@app.route("/api/manager/shop", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_shop():
    # 获取店铺信息
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        data0 = db.session.execute('select * from manager where telephone="%s"' % phone).fetchall()
        Data = data0[0][0]
        print(Data)
        data = db.session.execute('select * from fastfood_shop where manager_id="%d"'%Data).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(shop_name=data[i][0], price=data[i][1], sale=data[i][2])
            Data.append(dic)
        dic_test= dict(shop_name="测试删除修改", price=114, sale=514)
        Data.append(dic_test)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'POST' and request.json.get('action') == "add":
        rq = request.json
        shop_name = rq.get('shop_name')
        price = rq.get('price')
        m_sale_v = rq.get('m_sale_v')
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute('select * from manager where telephone="%s"' % phone).fetchall()
        Data = data[0][0]
        exist = db.session.execute('select * from fastfood_shop where shop_name="%s"' % shop_name).fetchall()
        if not exist:
            db.session.execute('insert fastfood_shop(shop_name,price,m_sale_v,manager_id) value("%s",%d,%d,%d)' % (
                shop_name, int(price), int(m_sale_v),int(Data)))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该店铺已存在")

    if request.method == 'POST' and request.json.get('action') == "change":
        rq = request.json
        shop_name = rq.get('shop_name')
        price = rq.get('price')
        m_sale_v = rq.get('m_sale_v')
        exist_change = db.session.execute('select * from fastfood_shop where shop_name="%s"' % shop_name).fetchall()
        if not exist_change:
            return jsonify(status=1000, msg="该店铺不存在,不能修改不存在的店铺")
        else:
            db.session.execute('update fastfood_shop set price="%d", m_sale_v="%d" where shop_name="%s" ' % (
                int(price), int(m_sale_v), shop_name))
            db.session.commit()
            return jsonify(status=200, msg="修改成功")
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        exist_delete = db.session.execute('select * from fastfood_shop where shop_name="%s"' % want_delete).fetchall()
        if not exist_delete:
            return jsonify(status=1000, msg="该店铺不存在,不能删除不存在的店铺")
        else:
            db.session.execute('delete from fastfood_shop where shop_name="%s"' % want_delete)
            db.session.commit()
            return jsonify(status=200, msg="删除成功")


@app.route("/api/manager/server", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_server():
    if request.method == 'GET':
        data = db.session.execute('select * from server').fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(service_id=data[i][0], service_name=data[i][1], fastfood_shop_name=data[i][2],)
            Data.append(dic)
        shop_range = db.session.execute('select shop_name from fastfood_shop').fetchall()
        Shop = []
        for i in range(len(shop_range)):
            dic = dict(shop_name=shop_range[i][0])
            Shop.append(dic)
        print(Shop)
        return jsonify(status=200, tabledata=Data, shop_range=Shop)
    if request.method == 'POST':
        rq = request.json
        service_id = rq.get('service_id')
        service_name = rq.get('service_name')
        fastfood_shop_name = rq.get('fastfood_shop_name')
        exist = db.session.execute('select * from server where service_id="%s"' % service_id).fetchall()
        if not exist:
            db.session.execute('insert server(service_id,service_name,fastfood_shop_name) value("%s","%s","%s")' % (
                service_id, service_name, fastfood_shop_name))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该编号已存在")
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        db.session.execute('delete from server where service_id="%s"' % want_delete)
        db.session.commit()
        return jsonify(status=200, msg="解雇成功")


@app.route("/api/manager/dispatcher", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_dispatcher():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        data0 = db.session.execute('select * from manager where telephone="%s"' % phone).fetchall()
        Data00 =data0[0][0]
        data = db.session.execute('select * from dispatcher where manager_id="%d"'% Data00).fetchall()
        Data = []

        for i in range(len(data)):
            dic = dict(dispatcher_id=data[i][0], dispatcher_name=data[i][1], dispatcher_phone=data[i][2])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'POST':
        rq = request.json
        dispatcher_id = rq.get('dispatcher_id')
        dispatcher_name = rq.get('dispatcher_name')
        dispatcher_phone = rq.get('dispatcher_phone')
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute('select * from manager where telephone="%s"' % phone).fetchall()
        manager_id=data[0][0]
        exist = db.session.execute('select * from dispatcher where dispatcher_id="%s"' % dispatcher_id).fetchall()
        if not exist:
            db.session.execute(
                'insert dispatcher(dispatcher_id,dispatcher_name,dispatcher_phone,manager_id) value("%s","%s","%s","%s")' % (
                    dispatcher_id, dispatcher_name, dispatcher_phone,manager_id))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该编号已存在")
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        db.session.execute('delete from dispatcher where dispatcher_id="%s"' % want_delete)
        db.session.commit()
        return jsonify(status=200, msg="解雇成功")


@app.route("/api/manager/wuliu", methods=["GET"])
@cross_origin()
def manager_wuliu():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        data0 = db.session.execute('select * from manager where telephone="%s"' % phone).fetchall()
        Data =data0[0][0]
        data = db.session.execute('select * from wuliu where manager_id="%d"'%Data).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], cons_phone=data[i][1], disp_id=data[i][2], deliver_time=data[i][3])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/manager/unsend", methods=["GET", "POST"])
@cross_origin()
def manager_unsend():
    if request.method == 'GET':
        data = db.session.execute('select * from oorder ').fetchall()

        Data = []
        for i in range(len(data)):
            exist = db.session.execute('select * from wuliu where order_id="%s"' % data[i][0]).fetchall()
            if not exist:
                dic = dict(order_id=data[i][0], shop_name=data[i][1], price=data[i][2], orderway=data[i][3],
                       cons_phone=data[i][4],
                       cons_name=data[i][5], cons_addre=data[i][6], create_time=data[i][7])
                Data.append(dic)

        disp_range = db.session.execute('select * from dispatcher').fetchall()  # 获取所有的送货员就id，供选择
        Disp_range = []
        for i in range(len(disp_range)):
            dic = dict(disp_id=disp_range[i][0])
            Disp_range.append(dic)
        return jsonify(status=200, tabledata=Data, disp_range=Disp_range)
    if request.method == 'POST':
        rq = request.json
        order_id = rq.get('order_id')
        disp_id = rq.get('dispatcher_id')
        deliver_time = rq.get('deliver_time')
        phone=get_token_phone(request.headers.get('token'))
        cons_phone = db.session.execute('select cons_phone from oorder where order_id="%d"' % int(order_id)).first()
        data = db.session.execute('select * from manager where telephone="%s"' % phone).fetchall()
        manager_id = data[0][0]
        db.session.execute('insert wuliu( order_id, cons_phone,disp_id,deliver_time,manager_id) value(%d,"%s","%s","%s","%d")' % (
            int(order_id), cons_phone[0], disp_id, deliver_time,manager_id))
        db.session.commit()
        return jsonify(status=200, msg="成功派发")


@app.route("/api/manager/cheap", methods=["GET"])
@cross_origin()
def manager_cheap():
    if request.method == 'GET':
        data = db.session.execute('select * from cheap_order').fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
                       cons_phone=data[i][4],
                       cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/manager/expensive", methods=["GET"])
@cross_origin()
def manager_expensive():
    if request.method == 'GET':
        data = db.session.execute('select * from expensive_order').fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
                       cons_phone=data[i][4],
                       cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/manager/food", methods=["GET"])
@cross_origin()
def manager_food():
    if request.method == 'GET':
        data = db.session.execute('select shop_name,m_sale_v from fastfood_shop group by shop_name having m_sale_v>50').fetchall()
        data1=db.session.execute('select shop_name from (select * from fastfood_shop where price<13)as a where m_sale_v>20').fetchall()
        Data = []
        len1=len(data1)
        len0=len(data)
        lenl=len0
        lens=len1
        if(len0<=len1):
            lenl=len1
            lens=len0
        for i in range(lenl):
            if(i<lens):
                dic = dict(food=data[i][0], sale=data[i][1], food1=data1[i][0])
                Data.append(dic)
            else:
                dic=dict(food=data[i][0], sale=data[i][1],food1=" ")
                Data.append(dic)
        return jsonify(status=200, tabledata=Data)

if __name__ == '__main__':
    app.run(debug=True)
