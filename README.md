# futures-collect
 期货数据采集

 采用新浪的数据源，采集5分钟成交数据

获取数据的url如下：
https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_M2001_5_1565347970270=/InnerFuturesNewService.getFewMinLine?symbol=M2001&type=5
其中_M2001_5_1565347970270为带时间戳的唯一变量名，M2001为合约名，type=5为5分钟


