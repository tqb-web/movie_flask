    $(document).ready(function() {
      $('#update-info-form').submit(function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
        var formData = $(this).serialize(); // 获取表单数据
        $.post('/update1', formData, function(response) {
          // 处理更新成功的消息
          showMessage(response.message);
        });
      });
    });

    function showMessage(message) {
      // 显示消息
      var messageElement = $('.message');
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



//2
    $(document).ready(function() {
      $('#change-password-form').submit(function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
        var formData = $(this).serialize(); // 获取表单数据
        $.post('/changepassword', formData, function(response) {
          // 处理更新成功的消息
          showMessage(response.message);
        });
      });
    });

$(function() {
  $('#username').on('input', function() {
    var username = $(this).val();
    $.ajax({
      url: '/check_username_afterLogin',
      method: 'POST',
      data: {username: username},
      success: function(response) {
        if (response.exists) {
            $('#username-exist').show();
        } else {
            $('#username-exist').hide();
        }
      },
      error: function() {
        console.log('请求失败');
      }
    });
  });
});

$(function() {
  $('#email').on('input', function() {
    var email = $(this).val();
    $.ajax({
      url: '/check_email',
      method: 'POST',
      data: {email: email},
      success: function(response) {
        if (response.exists) {
            $('#email-exist').show();
        } else {
            $('#email-exist').hide();
        }
      },
      error: function() {
        console.log('请求失败');
      }
    });
  });
});

$(function() {
  $('#phone').on('input', function() {
    var phone = $(this).val();
    $.ajax({
      url: '/check_phone',
      method: 'POST',
      data: {phone: phone},
      success: function(response) {
        if (response.exists) {
            $('#phone-exist').show();
        } else {
            $('#phone-exist').hide();
        }
      },
      error: function() {
        console.log('请求失败');
      }
    });
  });
});


$(document).ready(function() {
  $('#new_password').keyup(function() {
    var password = $(this).val();
    var regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;   //包括字母和数字，且长度至少为8位数
    if (!regex.test(password)) {
     $('#submit-btn').prop('disabled', true);
      $('#password-message').text('密码至少包括一个字母和一个数字，且长度至少为8位。');
    } else {
        $('#submit-btn').prop('disabled', false);
      $('#password-message').text('');
    }
  });
});


//$(document).ready(function() {
//  // 给上传头像按钮绑定点击事件
//  $("#uploadAvatarBtn").click(function() {
//    uploadAvatar();
//  });
//  });
//
//  // 上传头像函数
// function uploadAvatar() {
//  var file = $("#avatarFileInput")[0].files[0];
//    var allowedTypes = ["image/jpeg", "image/png"];
//    var fileType = file.type;
//    var maxSize = 2 * 1024 * 1024; // 2MB
//    if (!allowedTypes.includes(fileType)) {
//      alert("只能上传JPEG或PNG文件");
//      return;
//    }
//    if (file.size > maxSize) {
//      alert("文件太大了，最大只能上传2MB");
//      return;
//    }
//  var formData = new FormData();
//  formData.append("avatar", file);
//  $.ajax({
//    url: "/upload_avatar",
//    method: "POST",
//    data: formData,
//    contentType: false,
//    processData: false,
//    success: function (response) {
//      console.log("头像上传成功");
//    },
//    error: function (error) {
//      console.error("头像上传失败", error);
//    },
//  });
//}


//window.onload = function() {
//  const inpFile = document.querySelector('input[type="file"]');
//  const img = document.querySelector('.preview');
////  const btn = document.querySelector('button');
//const btn = document.querySelector('#uploadAvatarBtn');
//  inpFile.onchange = (e) => {
//      const file = e.target.files[0];
//      const reader = new FileReader();
//      reader.onload = (e) => {
//          img.src = e.target.result;
//      };
//      reader.readAsDataURL(file);
//  };
//  btn.onclick = () => {
//    const cutInfo = {
//        x: 50,
//        y: 50,
//        cutWidth: 30,
//        cutHeight: 30,
//        width: 50,
//        height: 50
//    }
//    const canvas = document.createElement('canvas')
//    canvas.width = cutInfo.width;
//    canvas.height = cutInfo.height;
//    const ctx = canvas.getContext('2d');
//    ctx.drawImage(img, cutInfo.x, cutInfo.y, cutInfo.cutWidth, cutInfo.cutHeight, 0, 0, cutInfo.width, cutInfo.height);
//    canvas.toBlob((blob) => {
//    new File([blob], 'avatar.jpg', {
//        type: 'image/jpeg'
//    })
//    }, 'image/jpeg');
//    document.getElementById('result').appendChild(canvas);
//  };
//};

