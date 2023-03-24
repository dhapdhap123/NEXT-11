const { default: fetch } = require("node-fetch");

const url =
  "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst";
const API_KEY =
  "H3tKiYEok/bQCrMJShz209BSaVhb2En6p6oB1XAX2X6bYJwu6F/EjdmqRR9RCLtUY1clf2j3qSckt/KYtyh/Uw==";
const Data = {
  serviceKey: API_KEY,
  numsOfRows: 1000,
  dataType: "JSON",
  base_date: request_day,
  base_time: request_time,
};
const otherPram = {
  headers: {
    "content-type": "application/json; charset=utf-8",
  },
  body: Data,
  method: "GET",
};

let now = new Date();
let year = String(now.getFullYear()).substring(2, 4); // 년도
let month = String(now.getMonth() + 1); // 월
if (month.length === 1) {
  month = "0" + month;
}
let date = String(now.getDate()); // 날짜
let hour = now.getHours(); // 시간
let minute = now.getMinutes(); // 분

const weather_request = () => {
  const request_day = year + month + date;
  const hour_str = String(hour);
  let new_hour = hour - 1;

  if (new_hour < 0) {
    new_hour = 11;
  }
  if (String(new_hour).length === 1) {
    new_hour = "0" + String(new_hour);
  }
  if (hour_str.length === 1) {
    hour = "0" + hour_str;
  }

  if (0 <= minute && minute <= 15) {
    const request_time = `${new_hour}00`;
    fetch(url, otherPram).then((response) => console.log(response));
  } else if (15 < minute && minute <= 45) {
    const request_time = `${new_hour}30`;
    fetch(url, otherPram).then((response) => console.log(response));
  } else if (45 < minute && minute <= 59) {
    const request_time = `${hour}00`;
    fetch(url, otherPram).then((response) => console.log(response));
  } else {
    console.log("error");
  }
  console.log(request_day);
};
weather_request();

/*
if (hour.length === 1) {
  hour = "0" + hour;
}
if (minute.length === 1) {
  minute = "0" + minute;
}


*/
