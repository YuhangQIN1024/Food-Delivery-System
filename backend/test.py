from flask import Flask

app = Flask(__name__)  # 创建app


@app.route('/index/<int:nid>',methods=['GET','POST'])
def index(nid):
    print("int类型: ", nid)
    return "返回结果是: int类型的nid"

if __name__ == '__main__':
    app.run()  # 运行
