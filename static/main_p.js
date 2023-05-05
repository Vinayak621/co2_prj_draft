const loanAmountInput = document.querySelector(".loan-amount");
const interestRateInput = document.querySelector(".interest-rate");
const loanTenureInput = document.querySelector(".loan-tenure");

const loanEMIValue = document.querySelector(".loan-emi .value");
const totalInterestValue = document.querySelector(".total-interest .value");
const totalAmountValue = document.querySelector(".total-amount .value");

const calculateBtn = document.querySelector(".calculate-btn");

let loanAmount = parseFloat(loanAmountInput.value);
let interestRate = parseFloat(interestRateInput.value);
let loanTenure = parseFloat(loanTenureInput.value);

let  renew = loanAmount*1500;
let  carbon = interestRate*88.56;

let myChart;

const displayChart = (totalInterestPayableValue) => {
  const ctx = document.getElementById("myChart").getContext("2d");
  myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["Savings", "Total tax"],
      datasets: [
        {
          data: [totalInterestPayableValue, loanTenure],
          backgroundColor: ["#e63946", "#14213d"],
          borderWidth: 0,
        },
      ],
    },
  });
};

const updateChart = (totalInterestPayableValue) => {
  myChart.data.datasets[0].data[0] = totalInterestPayableValue;
  myChart.data.datasets[0].data[1] = loanTenure;
  myChart.update();
};

const refreshInputValues = () => {
  loanAmount = parseFloat(loanAmountInput.value);
  interestRate = parseFloat(interestRateInput.value);
  loanTenure = parseFloat(loanTenureInput.value);
  renew = loanAmount*1500;
  carbon = interestRate*88.56;
};

const calculateEMI = () => {
  
  refreshInputValues();
  let totsav =renew+carbon;

  return totsav;
};

const updateData = (totsav) => {
  loanEMIValue.innerHTML = Math.round(totsav);

  
  totalAmountValue.innerHTML = Math.round(carbon);

  totalInterestValue.innerHTML = Math.round(renew);
  
  if (myChart) {
    updateChart(totsav);
  } else {
    displayChart(totsav);
  }
};

const init = () => {
  let totsav = calculateEMI();
  updateData(totsav);
};

init();

calculateBtn.addEventListener("click", init);
