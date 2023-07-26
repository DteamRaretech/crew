// モーダル表示をトリガーとするボタンの要素を取得
const modalButton = document.getElementById("modalButton");

// モーダル要素を取得
const modal = document.getElementById("myModal");

// モーダルを閉じる要素を取得
const closeSpan = document.getElementsByClassName("close")[0];

// モーダル表示をトリガーとするボタンにクリックイベントを追加
modalButton.addEventListener("click", () => {
  modal.style.display = "block";
});

// モーダルを閉じる要素にクリックイベントを追加
closeSpan.addEventListener("click", () => {
  modal.style.display = "none";
});

// モーダル外の領域をクリックしてもモーダルを閉じる
window.addEventListener("click", (event) => {
  if (event.target == modal) {
    modal.style.display = "none";
  }
});
