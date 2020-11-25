htmlcNumpad_Numbers = document.getElementsByClassName("Numpad"); // 페이지의 번호 버튼들
htmlcBack_Space = document.getElementById("back"); // 페이지의 백스페이스
htmlcClear = document.getElementById("clear"); // 페이지의 전체 지우기
htmlcInput = document.getElementById("Num_input"); // 페이지의 번호 입력칸

function Type_in(_str) {
    htmlcInput.innertext += _str;
}


htmlcNumpad_Numbers[0].onclick = Type_in("1");
htmlcNumpad_Numbers[1].onclick = Type_in("2");
htmlcNumpad_Numbers[2].onclick = Type_in("3");
htmlcNumpad_Numbers[3].onclick = Type_in("4");
htmlcNumpad_Numbers[4].onclick = Type_in("5");
htmlcNumpad_Numbers[5].onclick = Type_in("6");
htmlcNumpad_Numbers[6].onclick = Type_in("7");
htmlcNumpad_Numbers[7].onclick = Type_in("8");
htmlcNumpad_Numbers[8].onclick = Type_in("9");
htmlcNumpad_Numbers[9].onclick = Type_in("0");