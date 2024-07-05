FunAsr
----

模型使用的是阿里的 [FunASR](https://github.com/alibaba-damo-academy/FunASR), 这里做了一个http 服务，加上一些文件转换，方便对接一些服务使用。

### 使用

模型文件目录推荐映射出来，因为模型在线下载的。一共差不多 2g 的

```bash
docker run -d \
--restart=always -it \
--name fun-asr \
-p 5001:5001 \
-v $PWD/models:/models \
yaming116/fun-asr:latest
```

部署完成之后，等待模型下载完成之后，可以访问 ip:5001, 有一个测试界面可以使用。 

华为测试音频链接： 
https://sis-sample-audio.obs.cn-north-1.myhuaweicloud.com/16k16bit.mp3

### 接口

```
#:5001/api
#入参
file： 音频文件


#返回参数
{
    "code": 0,
    "data": [
        {
            "key": "rand_key_1qeoePtwBldGD",
            "text": "华为致力于把数字世界带入每个人、每个家庭、每个组织，构建万物互联的智能世界。",
    ],
    "filename": "/funAsr/static/tmp/16k16bit.mp3",
    "msg": "ok"
}
```

### 公众号
可以关注我的公众号，一起交流 HomeAssistant 相关技术。
![](./IMG_8406.JPG)

## 其他
感谢 [https://github.com/jianchang512/stt](https://github.com/jianchang512/stt)