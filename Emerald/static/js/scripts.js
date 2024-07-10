
// REGISTER
document.getElementById("nextButton1").addEventListener("click", function() {
    document.getElementById("form1").style.display = "none";
    document.getElementById("form2").style.display = "block";
});

document.getElementById("back").addEventListener("click", function() {
    document.getElementById("form2").style.display = "none";
    document.getElementById("form1").style.display = "block";
});
// REISTER


// PROFILE

document.addEventListener('DOMContentLoaded', function () {
    const editBtn = document.getElementById('editBtn');
    const saveBtn = document.getElementById('saveBtn');
    const inputs = document.querySelectorAll('input[readonly]');

    saveBtn.disabled = true;
    saveBtn.classList.add('disabled');

    inputs.forEach(input => {
        input.addEventListener('keyup', function () {
            if (input.value !== input.defaultValue) {
                saveBtn.disabled = false;
                saveBtn.classList.remove('disabled');
            } else {
                saveBtn.disabled = true;
                saveBtn.classList.add('disabled');
            }
        });
    });

    editBtn.addEventListener('click', function () {
        inputs.forEach(input => {
            input.removeAttribute('readonly');
        });
    });
});

// PROFILE

let isLikeActive = false;
let isDislikeActive = false;

function toggleLikeIcon(element) {
  const likeIcon = element;
  const dislikeIcon = document.querySelector('.dislike i');

  if (!isLikeActive && !isDislikeActive) {
    likeIcon.classList.remove('bx-like');
    likeIcon.classList.add('bxs-like');
    isLikeActive = true;
    dislikeIcon.classList.remove('bxs-dislike');
    dislikeIcon.classList.add('bx-dislike');
    isDislikeActive = false;
  } else if (isLikeActive) {
    likeIcon.classList.remove('bxs-like');
    likeIcon.classList.add('bx-like');
    isLikeActive = false;
  } else if (isDislikeActive) {
    likeIcon.classList.remove('bx-like');
    likeIcon.classList.add('bxs-like');
    isLikeActive = true;
    dislikeIcon.classList.remove('bxs-dislike');
    dislikeIcon.classList.add('bx-dislike');
    isDislikeActive = false;
  }
}

function toggleDislikeIcon(element) {
  const dislikeIcon = element;
  const likeIcon = document.querySelector('.like i');

  if (!isDislikeActive && !isLikeActive) {
    dislikeIcon.classList.remove('bx-dislike');
    dislikeIcon.classList.add('bxs-dislike');
    isDislikeActive = true;
    likeIcon.classList.remove('bxs-like');
    likeIcon.classList.add('bx-like');
    isLikeActive = false;
  } else if (isDislikeActive) {
    dislikeIcon.classList.remove('bxs-dislike');
    dislikeIcon.classList.add('bx-dislike');
    isDislikeActive = false;
  } else if (isLikeActive) {
    dislikeIcon.classList.remove('bx-dislike');
    dislikeIcon.classList.add('bxs-dislike');
    isDislikeActive = true;
    likeIcon.classList.remove('bxs-like');
    likeIcon.classList.add('bx-like');
    isLikeActive = false;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const likeButtons = document.querySelectorAll('.like i');
  const dislikeButtons = document.querySelectorAll('.dislike i');

  likeButtons.forEach(button => {
    button.addEventListener('click', function() {
      toggleLikeIcon(button);
    });
  });

  dislikeButtons.forEach(button => {
    button.addEventListener('click', function() {
      toggleDislikeIcon(button);
    });
  });
});


document.getElementById('search-form').addEventListener('submit', function() {
  document.getElementById('submit').classList.add('button-loading');
});
