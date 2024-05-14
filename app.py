
from funasr import AutoModel
import logging
from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from gevent.pywsgi import WSGIServer, WSGIHandler, LoggingLogAdapter
from logging.handlers import RotatingFileHandler
import warnings
warnings.filterwarnings('ignore')

ROOT_DIR = os.getcwd()
STATIC_DIR = os.path.join(ROOT_DIR, 'static')
TMP_DIR = os.path.join(STATIC_DIR, 'tmp')
# model_conf

os.environ['MODELSCOPE_CACHE'] = '/funAsr'
# os.environ['MODELSCOPE_CACHE'] = '/Users/sunshanming/localHub'
model = AutoModel(
    model="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    punc_model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
    spk_model="iic/speech_campplus_sv_zh-cn_16k-common",
    device='cpu'
)


class CustomRequestHandler(WSGIHandler):
    def log_request(self):
        pass


app = Flask(__name__)

# 配置日志
app.logger.setLevel(logging.WARNING)  # 设置日志级别为 INFO
# 创建 RotatingFileHandler 对象，设置写入的文件路径和大小限制
file_handler = RotatingFileHandler(os.path.join(ROOT_DIR, 'funAsr.log'), maxBytes=1024 * 1024, backupCount=5)
# 创建日志的格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 设置文件处理器的级别和格式
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)
# 将文件处理器添加到日志记录器中
app.logger.addHandler(file_handler)



@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)


@app.route('/')
def index():
    return render_template("index.html", language='zh')


@app.route('/upload', methods=['POST'])
def upload():
    try:
        # 获取上传的文件
        audio_file = request.files['audio']
        # 如果是mp4
        noextname, ext = os.path.splitext(audio_file.filename)
        ext = ext.lower()
        # 如果是视频，先分离
        wav_file = os.path.join(TMP_DIR, f'{noextname}{ext}')
        if os.path.exists(wav_file) and os.path.getsize(wav_file) > 0:
            return jsonify({'code': 0, 'msg': 'zh', "data": os.path.basename(wav_file)})
        msg = ""


        audio_file.save(wav_file)

        # 返回成功的响应
        return jsonify({'code': 0, 'msg': '上传成功' + msg, "data": os.path.basename(wav_file)})
    except Exception as e:
        app.logger.error(f'[upload]error: {e}')
        return jsonify({'code': 2, 'msg': '上传失败'})


@app.route('/api',methods=['GET','POST'])
def api():
    source_file = ''
    try:
        # 获取上传的文件

        audio_file = None
        if request.form.get('wav_name') is not None:
            source_file = os.path.join(TMP_DIR, request.form.get('wav_name') )

        else:
            audio_file = request.files.get("file") or request.form.get("file")
            noextname, ext = os.path.splitext(audio_file.filename)
            ext = ext.lower()
            source_file = os.path.join(TMP_DIR, f'{noextname}{ext}')
            if not os.path.exists(source_file) or os.path.getsize(source_file) == 0:
                audio_file.save(source_file)

        noextname, ext = os.path.splitext(source_file)
        print(f'{source_file=}')


        res = model.generate(
            input= source_file,
            hotword="达摩院 磨搭",
        )
        return jsonify({"code": 0, "msg": 'ok', "data": res, 'filename': f'{noextname}{ext}'})
    except Exception as e:
        print(e)
        app.logger.error(f'[api]error: {e}')
        return jsonify({'code': 2, 'msg': str(e)})
    finally:
        os.remove(source_file)


if __name__ == '__main__':
    http_server = None
    try:
        try:
            web_address = '0.0.0.0:5001'
            host = web_address.split(':')
            http_server = WSGIServer((host[0], int(host[1])), app, handler_class=CustomRequestHandler)

            app.logger.info(f" http://{web_address}")

            http_server.serve_forever(stop_timeout=10)
        finally:
            if http_server:
                http_server.stop()
    except Exception as e:
        if http_server:
            http_server.stop()
        print("error:" + str(e))
        app.logger.error(f"[app]start error:{str(e)}")
