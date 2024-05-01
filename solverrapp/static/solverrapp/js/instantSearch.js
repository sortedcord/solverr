const result_list = document.getElementById('result-list');
const result_div = document.getElementById('search-results');

const sym_translate = {
    'alpha':'α',
    'belong':'∈',
    'beta':'β',
    'infinity': '∞',
    'deg':'°',
    'notequal':'≠',
    'greaterthanequal':'≥',
    'lessthanequal':'≤',
    'gamma':'γ',
    'delta':'Δ',
    'epsilon':'ε',
    'theta':'θ',
    'lambda':'λ',
    'mu':'μ',
    'pi':'π',
    'SIGMA':'Σ',
    'sigma':'σ',
    'OMEGA':'Ω',
    'omega':'ω',
    'int':'∫',
    'sum':'∑',
}

const auto_translate = {
    '<=':'≤',
    '>=':'≥',
    '!=':'≠'
}



function update_result(json) {
    let inner_HT = "";
    for (let i in json.payload.data) {
         inner_HT += `<li class="list-group-item question"><a href="questions/${json.payload.data[i].index}/">${json.payload.data[i].text}</a></li>`
    }
    result_list.innerHTML = inner_HT;
    renderMathInElement(result_list, {
            delimiters: [
                { left: "$", right: "$", display: false },
                { left: "$$", right: "$$", display: true },
            ]
        });
}

function instantSearch() {
    let query = document.getElementById('query');

    const sym_insert = document.getElementById("symbol-insert");
    if (query.value.includes('\\')) {
        sym_insert.style.display = "block";

    } else {
        sym_insert.style.display = "none";
    }


    for (let i in sym_translate) {
        query.value = query.value.replace("\\"+i, sym_translate[i])
    }

    for (let i in auto_translate) {
        query.value = query.value.replace(i, auto_translate[i])
    }

    query = query.value.trim().replace(/ /g, '%20');
    if (query === '') {
        result_list.innerHTML="";
        result_div.style.display = "none";
        return;
    }
    else {
        result_div.style.display = 'Block';
    }

    fetch(`api/search/question?q=${query}`)
        .then((response) => response.json())
        .then((json) => update_result(json));
}


let timer;
input = document.getElementById('query');
input.addEventListener('keyup', function() {
    if (timer) {
        clearTimeout(timer);
    }
    timer = setTimeout(instantSearch, 1000);
});
