function add(x, y) {
    return x + y;
}

function _rds(len) {
    var retStr = '';
    for (i = 0; i < len; i++) {
        retStr += $_chars.charAt(Math.floor(Math.random() * _chars_len));
    }
    return retStr;
}

function _gas(data,key0,iv0){
    key0=key0.replace(/(^\s+)|(\s+$)/g, "");
    var key  = CryptoJS.enc.Utf8.parse(key0);
    var iv   = CryptoJS.enc.Utf8.parse(iv0);
    var encrypted =CryptoJS.AES.encrypt(data, key,{iv:iv, mode:CryptoJS.mode.CBC, padding:CryptoJS.pad.Pkcs7});
    return encrypted.toString();
}

function encryptAES(data, _p1){
    if(!_p1){
        return data;
    }
    var encrypted =_gas(_rds(64)+data, _p1, _rds(16));
    return encrypted;
}

function _etd2(password, pwdDefaultEncryptSalt) {
    _p0 = password;
    _p1 = pwdDefaultEncryptSalt;
    try{
        var _p2 = encryptAES(_p0,_p1);
        return _p2;
    }catch(e){
        return  _p0;
    }
}

function submitLoginForm(password, pwdDefaultEncryptSalt) {
    // var casLoginForm = $("#casLoginForm");
    // var username = casLoginForm.find("#username");
    // var password = casLoginForm.find("#password");
    //阻止表单button提交
    // e.preventDefault();

    // if (!checkRequired(username, "usernameError")) {
    //     username.focus();
    //     return false;
    // }

    // if (!checkRequired(password, "passwordError")) {
    //     password.focus();
    //     return false;
    // }
    _etd2(password, pwdDefaultEncryptSalt);


    // var isSliderCaptcha=$("#isSliderCaptcha").val();
    // reValidateDeal(isSliderCaptcha);

}