var mathInput = document.getElementById("math");
var englishInput = document.getElementById("english");
var submitBtn = document.getElementById("submitBtn");
var gradeTableBody = document.querySelector("#gradeTable tbody");

let grades = [];

submitBtn.addEventListener("click", function () {
  var math = parseFloat(mathInput.value);
  var english = parseFloat(englishInput.value);

  if (isNaN(math) || isNaN(english)) {
    alert("Please enter valid numbers for both Math and English. 請輸入有效數字");
    return;
  }

  grades.push({ math, english });

  addRowToTable(grades.length, math, english);
  updateColumnAverages();

  mathInput.value = "";
  englishInput.value = "";
});

function addRowToTable(index, math, english) {
  var avg = ((math + english) / 2).toFixed(2);
  var row = document.createElement("tr");

  row.innerHTML = `
    <td>${index}</td>
    <td>${math}</td>
    <td>${english}</td>
    <td>${avg}</td>
  `;

  gradeTableBody.appendChild(row);
}

function updateColumnAverages() {
  var mathTotal = 0, englishTotal = 0;

  grades.forEach(function(entry) {
    mathTotal += entry.math;
    englishTotal += entry.english;
  });

  var count = grades.length;
  var mathAvg = (mathTotal / count).toFixed(2);
  var englishAvg = (englishTotal / count).toFixed(2);
  var overallAvg = ((parseFloat(mathAvg) + parseFloat(englishAvg)) / 2).toFixed(2);

  document.getElementById("mathAvg").textContent = mathAvg;
  document.getElementById("englishAvg").textContent = englishAvg;
  document.getElementById("overallAvg").textContent = overallAvg;
}
