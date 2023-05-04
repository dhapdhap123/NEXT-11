play = (e) => {
  console.log(e.keyCode);
  console.log(typeof e.keyCode);
  const audio = document.querySelector(`audio[data-key="${e.keyCode}"]`);
  // 1. audio 변수를 html에서 select해주세요. audio변수는 누르는 키보드에 해당하는 keycode를 가지고 있는 음악파일(audio 태그)입니다.
  const key = document.querySelector(`li[data-key="${e.keyCode}"]`);
  // 2. key 변수를 html에서 select해주세요. key 변수는 누르는 키보드에 해당하는 keycode를 가진 li 태그입니다.

  console.log(audio, key);
  if (audio) {
    audio.play(); //audio.play()는 음원을 재생하는 함수이다.
    key.classList.add("play");
    //    3. 누른 key에 play 클래스를 부여하세요. HINT: classList를 사용하세요.
    //
  }
};

pause = (e) => {
  const audio = document.querySelector(`audio[data-key="${e.keyCode}"]`);
  // 1. audio 변수를 html에서 select해주세요. audio변수는 누르는 키보드에 해당하는 keycode를 가지고 있는 음악파일(audio 태그)입니다.
  const key = document.querySelector(`li[data-key="${e.keyCode}"]`);
  // 2. key 변수를 html에서 select해주세요. key 변수는 누르는 키보드에 해당하는 keycode를 가진 li 태그입니다.

  if (audio) {
    audio.currentTime = 0;
    audio.pause(); //audio.pause()는 음원을 일시정지하는 함수이다.
    key.classList.remove("play");
    //    3. 누른 key에 play 클래스를 제거하세요. HINT: classList를 사용하세요.
  }
};

// 4. 키보드를 눌렀을때 play함수가 실행되게, 키보드를 뗀다면 pause함수가 실행되게 해주세요.
//HINT: 전역객체 window와 addEventListener를 사용하세요.
// //
// const audio = document.getElementsByTagName("audio");
// const key = document.getElementsByTagName("li");
// //

// console.log(audio);

// for (let k in key) {
//   k.addeventListener("keyup", (e) => {
//     console.log(e);
//   });
// }
window.addEventListener("keydown", play);
window.addEventListener("keyup", pause);
