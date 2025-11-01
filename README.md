# x-location-watcher  
  
・Xのプロフィール欄にある「場所欄」「リンク欄」の監視  
・監視間隔は.ymlで指定  
  
・[secrets and variables]に「DISCORD_WEBHOOK_B」、「X_TARGET_URL」を追加する。  
　　・DISCORD_WEBHOOK_B：DISCRODサーバ設定＞連携サービス＞ウェブフック　　※指定したチャンネルに通知される。  
　　・X_TARGET_URL：監視したいXのURL　https://x.com/xxxxxx　（フルURLでいれる）  
  
・前回と変化があった場合のみDISCORDへ通知される。  
・取得した「場所欄・リンク欄」をキャッシュに保存して、スキャンしたときに差があればDISCORD通知。 

