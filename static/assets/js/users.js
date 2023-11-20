    $(document).ready(function() {
      $('.reset-password-form').submit(function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
        var formData = $(this).serialize(); // 获取表单数据
        $.post('/reset_password', formData, function(response) {
          // 处理更新成功的消息
          showMessage(response.message);
        });
      });
    });

    function showMessage(message) {
      // 显示消息
      var messageElement = $('#message');
      messageElement.html(message);
      messageElement.show();
      // 一定时间后隐藏消息
      setTimeout(function() {
        messageElement.hide();
      }, 3000); // 3 秒后隐藏
    }

$(document).ready(function() {
  var messageElement = $('#message');
  if (messageElement) {
    messageElement.hide();
  }
});


    $(document).ready(function() {
      $('.set-admin-form').submit(function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
        var formData = $(this).serialize(); // 获取表单数据
        $.post('/set_admin', formData, function(response) {
          // 处理更新成功的消息
          showMessage(response.message);
        });
      });
    });


 $(document).ready(function() {
      $('.cancel-admin-form').submit(function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
        var formData = $(this).serialize(); // 获取表单数据
        $.post('/cancel_admin', formData, function(response) {
          // 处理更新成功的消息
          showMessage(response.message);
        });
      });
    });

 $(document).ready(function() {
      $('.delete-user-form').submit(function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
        var formData = $(this).serialize(); // 获取表单数据
        $.post('/delete_user', formData, function(response) {
          // 处理更新成功的消息
          showMessage(response.message);
        });
      });
    });