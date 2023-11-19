//    window.onload = function() {
  const sortByVoteButton = document.getElementById('sort-by-vote');
  const sortByEvaluationButton = document.getElementById('sort-by-evaluation');
  const sortByCommentButton = document.getElementById('sort-by-comment');
  const sortByScoreButton = document.getElementById('sort-by-score');
  const sortByOrderButton = document.getElementById('sort-by-order');

  // 异步请求JSON数据
  fetch('/get_movies_data')
    .then(response => response.json())
    .then(data => {
      // 将获取到的JSON数据赋值给movies变量
      const movies = data.movies;

      // 定义排序函数
      function sortMovies() {
        // 获取排序方式和排序顺序
        const sortByVote = sortByVoteButton.checked;
        const sortByEvaluation = sortByEvaluationButton.checked;
        const sortByComment = sortByCommentButton.checked;
        const sortByScore = sortByScoreButton.checked;
        const sortByOrder = sortByOrderButton.checked;

//console.log(sortByVote, sortByEvaluation, sortByComment, sortByOrder);

        // 根据选中的方式排序电影列表
        if (sortByVote) {
          if (sortByOrder) {
            movies.sort((a, b) => a.vote - b.vote );
          } else {
            movies.sort((a, b) => b.vote  - a.vote );
          }
        } else if (sortByEvaluation) {
          if (sortByOrder) {
            movies.sort((a, b) => a.evaluation - b.evaluation);
          } else {
            movies.sort((a, b) => b.evaluation - a.evaluation);
          }
        } else if (sortByComment) {
          if (sortByOrder) {
            movies.sort((a, b) => a.comment - b.comment);
          } else {
            movies.sort((a, b) => b.comment - a.comment);
          }
          } else if (sortByScore) {
          if (sortByOrder) {
            movies.sort((a, b) => a.score - b.score);
          } else {
            movies.sort((a, b) => b.score - a.score);
          }
        } else {
          if (sortByOrder) {
            movies.sort((a, b) => a.order - b.order);
          } else {
            movies.sort((a, b) => b.order - a.order);
          }
        }

        // 更新电影列表的 HTML
        const movieListElement = document.getElementById('movie-list');
        movieListElement.innerHTML = movies.map(movie => `

              <tr>
                  <td style="width:5%;">${movie.id}</td>
                  <td style="width:15%;"><a href = "${movie.link}" target="_blank">${movie.name}</a></td>
                  <td style="width:15%;">${movie.year}</td>
                  <td style="width:10%;">${movie.vote}</td>
                  <td style="width:10%;">${movie.score}</td>
                  <td style="width:15%;">${movie.category}</td>
                  <td style="width:14%;">${movie.country}</td>
                  <td style="width:8%;">${movie.comment}</td>
                  <td style="width:8%;">${movie.evaluation}</td>
              </tr>

        `).join('');
      }

      // 监听按钮的点击事件
sortByVoteButton.addEventListener('click', () => {
    sortByVoteButton.checked = !sortByVoteButton.checked;
    sortByEvaluationButton.checked = false;
    sortByCommentButton.checked = false;
    sortByScoreButton.checked = false;
    sortByOrderButton.checked = true;

});

sortByEvaluationButton.addEventListener('click', () => {
    sortByEvaluationButton.checked = !sortByEvaluationButton.checked;
    sortByVoteButton.checked = false;
    sortByCommentButton.checked = false;
    sortByScoreButton.checked = false;
    sortByOrderButton.checked = true;
});

sortByCommentButton.addEventListener('click', () => {
    sortByCommentButton.checked  = !sortByCommentButton.checked;
    sortByVoteButton.checked = false;
    sortByEvaluationButton.checked = false;
    sortByScoreButton.checked = false;
    sortByOrderButton.checked = true;
});

sortByScoreButton.addEventListener('click', () => {
    sortByScoreButton.checked = !sortByScoreButton.checked;
    sortByVoteButton.checked = false;
    sortByEvaluationButton.checked = false;
    sortByCommentButton.checked = false;
    sortByOrderButton.checked = true;

});

sortByOrderButton.addEventListener('click', () => {
 if (sortByOrderButton.checked === true) {
    sortByOrderButton.textContent = '降序';
  } else {
    sortByOrderButton.textContent = '升序';
  }
     sortByOrderButton.checked = !sortByOrderButton.checked;
    sortMovies();
});

      // 页面加载时默认按票房排序
      sortMovies();
    });
//};


function removeActive() {
  const buttons = document.querySelectorAll('button');
  buttons.forEach(button => {
    button.classList.remove('active');
  });
}


//const sortByVoteButton = document.getElementById('sort-by-vote');
sortByVoteButton.addEventListener('click', () => {
  removeActive();
  sortByVoteButton.classList.add('active');
  // 进行排序操作
});

//const sortByEvaluationButton = document.getElementById('sort-by-evaluation');
sortByEvaluationButton.addEventListener('click', () => {
  removeActive();
  sortByEvaluationButton.classList.add('active');
  // 进行排序操作
});

//const sortByCommentButton = document.getElementById('sort-by-comment');
sortByCommentButton.addEventListener('click', () => {
  removeActive();
  sortByCommentButton.classList.add('active');
  // 进行排序操作
});

//const sortByScoreButton = document.getElementById('sort-by-score');
sortByScoreButton.addEventListener('click', () => {
  removeActive();
  sortByScoreButton.classList.add('active');
  // 进行排序操作
});
