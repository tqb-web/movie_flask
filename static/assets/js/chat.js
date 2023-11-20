//
//const chatInput = document.getElementById("chat-input");
//const chatForm = document.getElementById("chat-form");
//
//chatInput.addEventListener("keydown", function (event) {
//  if (event.key === "Enter" && !event.shiftKey) {
//    event.preventDefault();
//    chatForm.submit();
//  }
//});

//   $(function() {
//  $('#chat-form').submit(function(e) {
//    e.preventDefault();
//    var data = $('#chat-form').serialize();
//    var question = $('textarea[name="message"]').val();
//    $('#chat-form')[0].reset();
//        var inputMessage = $('<div class="chat-message"></div>');
//        var inputContent = $('<div class="chat-message-content question"></div>').html('<p>' + question + '</p>');
//        var inputAuthor = $('<img src="static/assets/img/wechat.jpg" style="width:40px;height:40px; border-radius: 50%;">');
//        inputMessage.append(inputAuthor);
//        inputMessage.append("   ");
//        inputMessage.append(inputContent);
//        $('#output-container-1').append(inputMessage);
//                $('#output-container-1').animate({
//          scrollTop: $('#output-container-1')[0].scrollHeight
//        }, 500);
//    $.ajax({
//      url: '/execute',
//      type: 'POST',
//      data: data,
//      success: function(response) {
//        var outputMessage = $('<div class="chat-message"></div>');
//        var outputContent = $('<div class="chat-message-content answer"></div>').html('<p>' + response + '</p>');
//        var outputAuthor = $('<img src="static/assets/img/bot.jpg" style="width:40px;height:40px; border-radius: 50%;">');
//        outputMessage.append(outputAuthor);
//        outputMessage.append("   ");
//        outputMessage.append(outputContent);
//        $('#output-container-1').append(outputMessage);
//        $('#output-container-1').animate({
//          scrollTop: $('#output-container-1')[0].scrollHeight
//        }, 500);
//      },
//      error: function(xhr, status, error) {
//        alert("服务器出现错误：" + error);
//      }
//    });
//  });
//});





//$(function() {
//  var chatHistory = localStorage.getItem('chatHistory');
//  if (chatHistory) {
//    $('#output-container-1').html(chatHistory);
//  }
//
//  $('#chat-form').submit(function(e) {
//    e.preventDefault();
//    var data = $('#chat-form').serialize();
//    var question = $('textarea[name="message"]').val();
//    $('#chat-form')[0].reset();
//    var inputMessage = $('<div class="chat-message"></div>');
//    var inputContent = $('<div class="chat-message-content question"></div>').html('<p>' + question + '</p>');
//    var inputAuthor = $('<img src="static/assets/img/wechat.jpg" style="width:40px;height:40px; border-radius: 50%;">');
//    inputMessage.append(inputAuthor);
//    inputMessage.append(" ");
//    inputMessage.append(inputContent);
//    $('#output-container-1').append(inputMessage);
//    $('#output-container-1').animate({
//      scrollTop: $('#output-container-1')[0].scrollHeight
//    }, 500);
//    $.ajax({
//      url: '/execute',
//      type: 'POST',
//      data: data,
//      success: function(response) {
//        var outputMessage = $('<div class="chat-message"></div>');
//        var outputContent = $('<div class="chat-message-content answer"></div>').html('<p>' + response + '</p>');
//        var outputAuthor = $('<img src="static/assets/img/bot.jpg" style="width:40px;height:40px; border-radius: 50%;">');
//        outputMessage.append(outputAuthor);
//        outputMessage.append(" ");
//        outputMessage.append(outputContent);
//        $('#output-container-1').append(outputMessage);
//        $('#output-container-1').animate({
//          scrollTop: $('#output-container-1')[0].scrollHeight
//        }, 500);
//
//        // 将对话记录保存在本地存储中
//        localStorage.setItem('chatHistory', $('#output-container-1').html());
//      },
//      error: function(xhr, status, error) {
//        alert("服务器出现错误：" + error);
//      }
//    });
//  });
//});

$(function() {
  var userId = localStorage.getItem('userId');
  if (userId) {
    var chatHistory = localStorage.getItem('chatHistory-' + userId);
    if (chatHistory) {
    var avatarUrl = $('#avatar-url').val();
      $('#output-container-1').html(chatHistory);
    }
  }

  $('#chat-form').submit(function(e) {
    e.preventDefault();
    var data = $('#chat-form').serialize();
    var question = $('textarea[name="message"]').val();
    $('#chat-form')[0].reset();
    var inputMessage = $('<div class="chat-message"></div>');
    var inputContent = $('<div class="chat-message-content question"></div>').html('<p>' + question + '</p>');
//    var inputAuthor = $('<img src="static/assets/avatar/avatar_' + currentUserId + '.png" style="width:40px;height:40px; border-radius: 50%;">');
    var avatarUrl = $('#avatar-url').val();
    var inputAuthor = $('<img src="' + avatarUrl + '" style="width:40px;height:40px; border-radius: 50%;">');
    inputMessage.append(inputAuthor);
    inputMessage.append(" ");
    inputMessage.append(inputContent);
    $('#output-container-1').append(inputMessage);
    $('#output-container-1').animate({
      scrollTop: $('#output-container-1')[0].scrollHeight
    }, 500);
    $.ajax({
      url: '/execute',
      type: 'POST',
      data: data + '&userId=' + userId,
      success: function(response) {
        var outputMessage = $('<div class="chat-message"></div>');
        var outputContent = $('<div class="chat-message-content answer"></div>').html('<p>' + response + '</p>');
        var outputAuthor = $('<img src="static/assets/img/bot.jpg" style="width:40px;height:40px; border-radius: 50%;">');
        outputMessage.append(outputAuthor);
        outputMessage.append(" ");
        outputMessage.append(outputContent);
        $('#output-container-1').append(outputMessage);
        $('#output-container-1').animate({
          scrollTop: $('#output-container-1')[0].scrollHeight
        }, 500);

        // 将对话记录保存在本地存储中
        localStorage.setItem('chatHistory-' + userId, $('#output-container-1').html());
//        localStorage.removeItem('chatHistory-' + userId)
      },
      error: function(xhr, status, error) {
        alert("服务器出现错误：" + error);
      }
    });
  });
});
