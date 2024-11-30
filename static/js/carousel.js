document.addEventListener("DOMContentLoaded", function () {
  const items = document.querySelectorAll(".carousel-item");
  const prevButton = document.querySelector(".carousel-button.prev");
  const nextButton = document.querySelector(".carousel-button.next");
  let currentIndex = 0;

  function showItem(index) {
    items.forEach((item) => item.classList.remove("active"));
    items[index].classList.add("active");
  }

  function nextItem() {
    currentIndex = (currentIndex + 1) % items.length;
    showItem(currentIndex);
  }

  function prevItem() {
    currentIndex = (currentIndex - 1 + items.length) % items.length;
    showItem(currentIndex);
  }

  nextButton.addEventListener("click", nextItem);
  prevButton.addEventListener("click", prevItem);

  // Автоматическое переключение каждые 5 секунд
  setInterval(nextItem, 5000);
});
