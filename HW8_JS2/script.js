// 用 getElementById 抓元素
var num1Input = document.getElementById("num1");
var num2Input = document.getElementById("num2");
var operatorSelect = document.getElementById("operator");
var calculateBtn = document.getElementById("calculateBtn");
var resultDisplay = document.getElementById("result");

// 四個基本運算 function
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) {
    return "Error: Cannot divide by 0!";
  }
  return a / b;
}

// 總控制函式
function calculate() {
  var a = parseFloat(num1Input.value);
  var b = parseFloat(num2Input.value);
  var operator = operatorSelect.value;
  var result;

  if (isNaN(a) || isNaN(b)) {
    resultDisplay.textContent = "Please enter valid numbers.";
    return;
  }

  switch (operator) {
    case "+":
      result = add(a, b);
      break;
    case "-":
      result = subtract(a, b);
      break;
    case "*":
      result = multiply(a, b);
      break;
    case "/":
      result = divide(a, b);
      break;
  }

  // 顯示結果：錯誤訊息直接顯示；否則保留小數2位
  if (typeof result === "string") {
    resultDisplay.textContent = result;
  } else {
    resultDisplay.textContent = "Result = " + result.toFixed(2);
  }
}

// 綁定 click 事件
calculateBtn.addEventListener("click", calculate);
