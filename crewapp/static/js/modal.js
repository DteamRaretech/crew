function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
  
    if (username === "" || password === "") {
      displayErrorModal("Please enter both username and password");
      return false; // フォームの送信を中止
    }
  
    // ログインの処理を行う場合は、ここに追加のコードを記述
  
    return true; // フォームを送信
  }
  
  function displayErrorModal(errorMessage) {
    var modal = document.getElementById("modal");
    var modalContent = document.querySelector(".modal-content");
    var errorMessageElement = document.getElementById("errorMessage");
  
    errorMessageElement.textContent = errorMessage;
    modal.style.display = "block";
  
    var closeBtn = document.getElementsByClassName("close")[0];
    closeBtn.onclick = function() {
      modal.style.display = "none";
    };
  
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };
  }
  