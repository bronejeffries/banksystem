
// document.addEventListener('load',function(e){
//
//
// },false)

$(document).ready(function(){
  let firstnameinput = document.getElementById('cname')
  let lastnameinput = document.getElementById('clname')
  let username_visible = document.getElementById('cuser_name')
  let user_name_hidden = document.getElementById('cuser_name_hidden')
  let account_name_visible = document.getElementById('caccount_name')
  let account_name_hidden = document.getElementById('caccount_name_hidden')
  let holder = ""
  let holder2 = ""
  let middlename = document.getElementById('cmname')

  lastnameinput.addEventListener('keyup',function(event){
    if (firstnameinput.value.length > 1) {
      holder = firstnameinput.value + lastnameinput.value
      if (middlename.value.length > 0) {
      holder2 = firstnameinput.value+" "+middlename.value+" "+lastnameinput.value
      }else {
      holder2 = firstnameinput.value+" "+lastnameinput.value
      }

      username_visible.value = holder
      user_name_hidden.value = holder

      account_name_visible.value = holder2
      account_name_hidden.value = holder2

    }

  },false);

});
