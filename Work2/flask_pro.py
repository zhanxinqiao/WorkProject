# # -*-coding:utf-8-*-
# from flask import Flask, request, Response, abort ,render_template
# from flask_cors import CORS
# # from ast import literal_eval
# import time
# import sys
# import json
# import traceback
# import request_pro
# #from gevent import pywsgi
#
# app = Flask(__name__)
# CORS(app)  # 允许所有路由上所有域使用CORS
#
#
# @app.route("/", methods=['POST', 'GET'])
# def inedx():
#     return '领英账号检测程序正在运行中'
#
#
# @app.route("/linkedin_check", methods=['POST', 'GET'])
# def get_result():
#     if request.method == 'POST':
#         text = request.data.decode("utf-8")
#     else:
#         text = request.args['text']
#
#     try:
#         print("输入参数", text)
#         arg = text.split(',')
#         num = (len(arg))
#         #传过来的号码切分之后遍历，每个检测逻辑写在下面的for循环里
#         for i in range(num):
#             if arg[i] == '16502000070':
#                 arg[i] = '已注册'
#             else:
#                 arg[i] = '未注册'
#
#         res = arg
#         result = {"code": "200", "msg": "响应成功", "data": res}
#     except Exception as e:
#         print(e)
#         result_error = {'errcode': -1}
#         result = json.dumps(result_error, indent=4, ensure_ascii=False)
#         # 这里用于捕获更详细的异常信息
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
#         # 提前退出请求
#         abort(Response("Failed!\n" + '\n\r\n'.join('' + line for line in lines)))
#     return Response(str(result), mimetype='application/json')
#
#
# if __name__ == "__main__":
#     app.run(host='127.0.0.1', port=1314, threaded=False)
#     #server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
#     #server.serve_forever()