    $(document).ready(function() {
      $('.feedback-form').submit(function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
        var formData = $(this).serialize(); // 获取表单数据
        $.post('/feedback', formData, function(response) {
          // 处理更新成功的消息
          showMessage(response.message);
        });
      });
    });

    function showMessage(message) {
      // 显示消息
      var messageElement = $('#message1');
      messageElement.html(message);
      messageElement.show();
      // 一定时间后隐藏消息
      setTimeout(function() {
        messageElement.hide();
      }, 3000); // 3 秒后隐藏
    }

$(document).ready(function() {
  var messageElement = $('#message1');
  if (messageElement) {
    messageElement.hide();
  }
});
