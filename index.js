/*
초단기 예보, 초단기 실황 API
*/
const url_short =
  "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst";
const url_long =
  "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst";
const API_KEY =
  "H3tKiYEok%2FbQCrMJShz209BSaVhb2En6p6oB1XAX2X6bYJwu6F%2FEjdmqRR9RCLtUY1clf2j3qSckt%2FKYtyh%2FUw%3D%3D";
// 기상청 API 필요사항인 x, y 변환
function convertXY(v1, v2) {
  const { PI, tan, log, cos, pow, floor, sin } = Math;
  //
  // LCC DFS 좌표변환을 위한 기초 자료
  //
  const RE = 6371.00877; // 지구 반경(km)
  const GRID = 5.0; // 격자 간격(km)
  const SLAT1 = 30.0; // 투영 위도1(degree)
  const SLAT2 = 60.0; // 투영 위도2(degree)
  const OLON = 126.0; // 기준점 경도(degree)
  const OLAT = 38.0; // 기준점 위도(degree)
  const XO = 43; // 기준점 X좌표(GRID)
  const YO = 136; // 기1준점 Y좌표(GRID)

  const DEGRAD = PI / 180.0;

  const re = RE / GRID;
  const slat1 = SLAT1 * DEGRAD;
  const slat2 = SLAT2 * DEGRAD;
  const olon = OLON * DEGRAD;
  const olat = OLAT * DEGRAD;

  let sn = tan(PI * 0.25 + slat2 * 0.5) / tan(PI * 0.25 + slat1 * 0.5);
  sn = log(cos(slat1) / cos(slat2)) / log(sn);
  let sf = tan(PI * 0.25 + slat1 * 0.5);
  sf = (pow(sf, sn) * cos(slat1)) / sn;
  let ro = tan(PI * 0.25 + olat * 0.5);
  ro = (re * sf) / pow(ro, sn);
  const rs = {};
  let ra, theta;

  rs.lat = v1;
  rs.lon = v2;
  ra = tan(PI * 0.25 + v1 * DEGRAD * 0.5);
  ra = (re * sf) / pow(ra, sn);
  theta = v2 * DEGRAD - olon;
  if (theta > PI) theta -= 2.0 * PI;
  if (theta < -PI) theta += 2.0 * PI;
  theta *= sn;
  rs.x = floor(ra * sin(theta) + XO + 0.5);
  rs.y = floor(ro - ra * cos(theta) + YO + 0.5);

  return [rs.x, rs.y];
}
// gps 정보 가져오고, kakaomap 생성, weather_request 실행
function onGeoOk(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  const lat_lon = convertXY(latitude, longitude);
  const x_lat = lat_lon[0];
  const x_lon = lat_lon[1];

  weather_request(x_lat, x_lon);
}
function onGeoError() {
  alert("geolocation error");
}
// 시간 정보 가져오기
function getTime() {
  let now = new Date();
  let year = String(now.getFullYear()); // 년도
  let month = String(now.getMonth() + 1); // 월
  if (month.length === 1) {
    month = "0" + month;
  }
  let date = String(now.getDate()); // 날짜
  let hour = now.getHours(); // 시간
  let minute = now.getMinutes(); // 분
  return { year: year, month: month, date: date, hour: hour, minute: minute };
}
// 기상청 API 요청
function weather_request(x_lat, y_lon) {
  const { year, month, date, hour } = getTime();

  const request_day = year + month + date;
  const hour_str = String(hour);

  if (hour_str.length === 1) {
    hour = "0" + hour_str;
  }
  const request_time = `${hour}00`;
  make_output(request_day, request_time, x_lat, y_lon);
}
// whole url_long 만들고 request, response 값 array로 가져옴
function getPositionWeather() {
  navigator.geolocation.getCurrentPosition(onGeoOk, onGeoError);
}
// main.js()
getPositionWeather();

function make_output(request_day, request_time, x_lat, y_lon) {
  // 초단기 실황 fetch/error 잡기
  let whole_url = `${url_short}?serviceKey=${API_KEY}&pageNo=1&numOfRows=1000&dataType=JSON&base_date=${request_day}&base_time=${request_time}&nx=${x_lat}&ny=${y_lon}`;
  fetch(whole_url).then((response) => {
    return response.json().then((json) => {
      if (json.response.header.resultMSG === undefined) {
        const new_request_time =
          String(Number(request_time.slice(0, 2)) - 1) + "00";
        whole_url = `${url_short}?serviceKey=${API_KEY}&pageNo=1&numOfRows=1000&dataType=JSON&base_date=${request_day}&base_time=${new_request_time}&nx=${x_lat}&ny=${y_lon}`;
        fetch_short_wheather(whole_url, new_request_time);
      } else {
        fetch_short_wheather(whole_url, request_time);
      }
    });
  });

  // 단기 예보 fetch/error 잡기
  whole_url = `${url_long}?serviceKey=${API_KEY}&pageNo=1&numOfRows=1000&dataType=JSON&base_date=${request_day}&base_time=${request_time}&nx=${x_lat}&ny=${y_lon}`;
  fetch(whole_url).then((response) => {
    return response.json().then((json) => {
      if (json.response.header.resultMSG === undefined) {
        const new_request_time =
          String(Number(request_time.slice(0, 2)) - 1) + "00";
        whole_url = `${url_long}?serviceKey=${API_KEY}&pageNo=1&numOfRows=1000&dataType=JSON&base_date=${request_day}&base_time=${new_request_time}&nx=${x_lat}&ny=${y_lon}`;
        fetch_long_wheather(whole_url, new_request_time);
      } else {
        fetch_long_wheather(whole_url, request_time);
      }
    });
  });
}

function fetch_short_wheather(whole_url, request_time) {
  fetch(whole_url)
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      return json.response.body.items.item;
    })
    .then((item) => {
      const item_obj = { T1H: "", RN1: "", REH: "", PTY: "", WSD: "" };
      for (let i in item) {
        for (let j in item_obj) {
          if (item[i].category === j) {
            item_obj[j] = item[i].obsrValue;
          }
        }
      }
      console.log(`${request_time.slice(0, 2)}시 기준 초단기 실황`, item_obj);
    });
}

function fetch_long_wheather(whole_url, request_time) {
  fetch(whole_url)
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      return json.response.body.items.item;
    })
    .then((item) => {
      const first_time = Number(request_time.slice(0, 2)) + 1;
      const item_obj = [];

      for (let i = 0; i < 6; i++) {
        item_obj.push({
          time: first_time + i,
          T1H: "",
          RN1: "",
          SKY: "",
          REH: "",
          PTY: "",
          LGT: "",
          WSD: "",
        });
      }

      for (let i in item) {
        // ex) i = 0, 1, ... , 60
        for (let j in item_obj) {
          // j = 0, 1, 2, 3, 4, 5
          if (
            // ex) item[i] = {"baseDate":"20230322","baseTime":"1130","category":"LGT","fcstDate":"20230322","fcstTime":"1200","fcstValue":"0","nx":55,"ny":127}
            String(item[i].fcstTime).slice(0, 2) === String(item_obj[j].time)
          ) {
            switch (item[i].category) {
              case "T1H":
                item_obj[j]["T1H"] = item[i]["fcstValue"];
                break;
              case "RN1":
                item_obj[j]["RN1"] = item[i]["fcstValue"];
                break;
              case "SKY":
                item_obj[j]["SKY"] = item[i]["fcstValue"];
                break;
              case "REH":
                item_obj[j]["REH"] = item[i]["fcstValue"];
                break;
              case "PTY":
                item_obj[j]["PTY"] = item[i]["fcstValue"];
                break;
              case "LGT":
                item_obj[j]["LGT"] = item[i]["fcstValue"];
                break;
              case "WSD":
                item_obj[j]["WSD"] = item[i]["fcstValue"];
                break;
              default:
                break;
            }
          }
        }
      }
      console.log(`${request_time.slice(0, 2)}시 기준 단기 예보`, item_obj);
    });
}
