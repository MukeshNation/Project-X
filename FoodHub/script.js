document.addEventListener('DOMContentLoaded', function() {
  const foodHub = document.createElement('div');
  foodHub.className = 'food-hub';
  foodHub.innerHTML = `<h1>Welcome to FoodHub</h1><p>Your ultimate destination for delicious recipes and food discoveries!</p><button onclick="addFood()">Add Food</button>`;
  document.body.appendChild(foodHub);

  function addFood() {
    alert('Food added! Check your favorites section to see new additions.');
  }
});