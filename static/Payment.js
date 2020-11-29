var localstorage = this.localStorage
var lType_of_payment = ['공차 쿠폰', '통신사 할인', '기프티콘'];
var lWhat_to_do = ['공차 쿠폰 번호를 입력해 주시오', '전화 번호를 입력해 주시오', '기프티콘 번호를 입력해 주시오'];
var lPic_src = ['../static/coupon_scan.jpg', '../static/membership_scan.jpg', '../static/gifticon_scan.jpg'];

function payment_type_set(_type) {
    localstorage.removeItem('Payment_type');
    localstorage.removeItem('Pic_src');

    localstorage.setItem('Payment_type', lType_of_payment[_type]);
    localstorage.setItem('Pic_src', lPic_src[_type]);
    if(_type == 0 || _type == 1) {
        localstorage.setItem('Is_Discount', '1');
    }
    return window.location.href = '../templates/payment_scan.html';
}

function cancel() {
    if(localstorage.getItem('Is_Discount')) {
        let paymenttype = localstorage.getItem('Payment_type')
        if(paymenttype == '공차 쿠폰' || paymenttype == '통신사 할인') {
            localstorage.removeItem('Is_Discount');
        }
    }
    return location.href = '../templates/payment_selection.html';
}