const modal = document.querySelector(".modal");

/* 모달 여는 버튼 Dom요소에 접근하기 */
const openBtn = document.querySelector(".open-button");
/* 모달 열 때의 실행할 함수 정의하기 */

function openModal() {
  modal.classList.remove("hidden");
}

/* 버튼 클릭했을 때 모달 활성화하는 함수 실행하기 */
openBtn.addEventListener("click", openModal);
/* 모달 닫는 Dom요소에 접근하기 */

const closeBtn = modal.querySelector(".close");
const overlay = modal.querySelector(".modal-overlay");

/* 모달 닫을 때의 실행할 함수 정의하기 */

function closeModal() {
  modal.classList.add("hidden");
}

/* 버튼 클릭했을 때 모달 비활성화하는 함수 실행하기 */

closeBtn.addEventListener("click", closeModal);
overlay.addEventListener("click", closeModal);
