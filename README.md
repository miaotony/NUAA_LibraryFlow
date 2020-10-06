# NUAA Library Flow

Crawling and visualization of human flow information in NUAA Library

图书馆人流量信息爬取与可视化

**数据来自[图书馆预约系统](http://kjcx.nuaa.edu.cn)**  

[TODO list](https://github.com/miaotony/NUAA_LibraryFlow/issues/1)  

**Under construction...**  

Welcome your issues and PRs!  

---  

## File info

- `crawler.py`    图书馆预约系统爬虫 NUAA Library Flow Crawler  
- `flow.py`       后端接口 backend API  
- `save_data.py`  保存数据到本地 （最新数据 `./data/latest/<date>.json` 及全部数据 `./data/all/<date>.json`）  Save data to the local storage  
- `.github/workflows/update_flow.yml`  GitHub Action 配置文件  

---  

## Usage  

### For local use  本地使用 

首先把代码拉到本地，安装依赖。  
请注意只需要拉取 master 分支的即可。  

```bash
git clone -b master --depth=1 https://github.com/miaotony/NUAA_LibraryFlow.git
cd NUAA_LibraryFlow
pip3 install -r requirements.txt
```

而后执行相应的程序即可，例如，想要把当前的数据保存到本地：

```bash
python3 save_data.py
```

运行环境：Python >= 3.6  

### For remote use  远程使用

目前已经基于 GitHub Action 实现了图书馆预约系统数据的定时自动爬取，并搭建了一个获取数据的接口。  

**API:** 

均为 GET 方法。  

`date` 为日期，格式如 `2020-10-07`。(`%Y-%m-%d`)  

某一天的最新数据：  

`https://libflow.miaotony.xyz/data/latest/date.json`

某一天的全部数据：   

`https://libflow.miaotony.xyz/data/all/date.json`

> 例如，获取2020年10月7日的数据，对应接口为  
> 
> https://libflow.miaotony.xyz/data/latest/2020-10-07.json  
> 
> https://libflow.miaotony.xyz/data/all/2020-10-07.json  


**Data format 数据格式：**  

```json
{
  "time": "2020-10-07 01:00:11",
  "data": [
    {
      "area": "MGG4F",
      "now": "1",
      "all": "140"
    },
    {
      "area": "JJL3F",
      "now": "8",
      "all": "280"
    },
    {
      "area": "JJL6F",
      "now": "3",
      "all": "150"
    },
    {
      "area": "TMH",
      "now": "1",
      "all": "70"
    },
    {
      "area": "JJL5F",
      "now": "3",
      "all": "255"
    },
    {
      "area": "MGG2F",
      "now": "0",
      "all": "186"
    },
    {
      "area": "MGG3F",
      "now": "0",
      "all": "205"
    },
    {
      "area": "JJL2F",
      "now": "5",
      "all": "180"
    },
    {
      "area": "JJL4F",
      "now": "9",
      "all": "260"
    }
  ]
}
```
- `time`    当前时间  
- `area`    区域名称（明故宫，将军路，天目湖）  
- `now`     当前预约人数  
- `all`     最大预约人数  

---  

## Copyright

**网络非法外之地，本项目相关技术内容仅供学习研究，请在合理合法范围内使用！**  
**The relevant technical content of this project is only for study and research, please use within the reasonable and legal scope!**  

License:  
[GNU Affero General Public License v3.0](LICENSE)  

未经允许不得商用！  
Non-commercial use!  

最终解释权归本项目开发者所有。  
The final interpretation right belongs to the developer of the project.  

Copyright © 2020 [MiaoTony](https://github.com/miaotony).  