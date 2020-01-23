# 用 Line Notify 發送每日星座

訂閱星座 Notify，發送運勢。


# 開發
## 註冊 Line Notify 服務

到[官方頁面](https://notify-bot.line.me/zh_TW/)註冊一個 Line Notify 服務

## 建立 config
/instance/config.py      
- CLIENT_ID  
- CLIENT_SECRET  
- CALLBACK_URL  
- HOROSCOPE_API_URL 

## Notify 訂閱頁面
提供使用者訂閱你的 Line Notify 服務，頁面會引導使用者到 Line Notify 的授權頁面。

## Notify callback 
若使用者成功訂閱服務，Line Notify 會發送一組 `code` 給指定的 callback url，再以這組 code 以及其他指定參數向 Line Notify 請求使用者的 access token。

## 儲存 access token
剛剛取得的 access token 需要存下來作為日後發送 notify 的依據，
本範例使用 Google Firestore，並建立一份 service_account 的 json 檔來處理身份驗證，或是可以參考官方文件 [Set up authentication](https://cloud.google.com/firestore/docs/quickstart-servers?hl=zh-tw)。


## 發送 Notify
串接 [Daily Horoscopes API](https://github.com/yuchitung/daily-horoscopes-api) ，取得當日運勢並發送給所有訂閱者

## 每日發送運勢
設定 cronjob，每日呼叫 https://domain/daily-notify


# Reference
[如何快速建置一個 LINE Notify 的服務](https://www.evanlin.com/go-line-notify/)
