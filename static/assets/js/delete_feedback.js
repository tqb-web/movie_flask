$(document).on('click', '.delete-feedback-btn', function() {
    var feedback_id = $(this).data('feedback-id');
    var button = $(this);
   var confirmed = confirm('确定要删除该反馈吗？');
    if (confirmed) {
        $.ajax({
            url: '/delete_feedback',
            method: 'POST',
            data: { feedback_id: feedback_id },
            success: function(response) {
                if (response.success) {
                    showMessage('删除成功!');
                    button.closest('tr').next('tr').remove(); // 删除反馈详情行
                    button.closest('tr').remove(); // 删除反馈行
                } else {
                    // 删除失败，显示错误提示
                    showMessage(response.message);
                }
            },
            error: function() {
                // 请求失败，显示错误提示
                console.log('请求失败');
            }
        });
    }
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