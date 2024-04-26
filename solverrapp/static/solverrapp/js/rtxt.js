const toolbar_buttons = {
    'image': [
        {
            name: 'image',                    
            code: '![Image Description](URL)',
            cursor: [-5, -2],
            display: '<i class="bi bi-image"></i>',
            description: 'Insert Image'
        },
    ],
    'equation': [
        {
            name: 'inline',
            code: '$ENTER LATEX EQUATION HERE$',
            cursor: [1, -2],
            display: '<i class="bi bi-text-wrap"></i>',
            description: 'Insert Inline Equation'
        },
        {
            name: 'block',
            code: '$$ENTER LATEX EQUATION HERE$$',
            cursor: [2, -3],
            display: '<i class="bi bi-justify"></i>',
            description: 'Insert Block Equation'
        },
    ],
    'exponents': [
        {
            name: 'superscript',
            code: '^{x}',
            cursor: [2, 3],
            display: '$a^{x}$',
            description: 'Superscript'
        },
        {
            name: 'subscript',
            code: '_{x}',
            cursor: [2, 3],
            display: '$a_{x}$',
            description: 'Subscript'
        },
        {
            name: 'radical',
            code: '\\sqrt{x}',
            cursor: [-3, -2],
            display: '$\\sqrt{x}$',
            description: 'Radical (Under root Sign)'
        },
    ],
    'operators': [
        {
            name: 'times',
            code: '\\times',
            cursor: 'end',
            display: '$\\times$',
            description: 'Multiplication'
        },
        {
            name: 'div',
            code: '\\div',
            cursor: 'end',
            display: '$\\div$',
            description: 'Division'
        },
        {
            name: 'fraction',
            code: '\\frac{NUM}{DENOM}',
            cursor: [6, 9],
            display: '$\\frac{a}{b}$',
            description: 'Insert Fraction'
        },
    ],
    'symbols': [
        {
            name: 'notequal',
            code: '\\neq',
            cursor: 'end',
            display: '$\\neq$',
            description: 'Not equal to'
        },
        {
            name: 'infinity',
            code: '\\infty',
            cursor: 'end',
            display: '$\\infty$',
            description: 'Infinity'
        },
    ],
};

function getButton(name) {
    var req_button = null;
    var req_group = null;
    for (const group in toolbar_buttons) {
        if (Object.hasOwnProperty.call(toolbar_buttons, group)) {
            toolbar_buttons[group].forEach(button => {
                if (button.name == name) {
                    req_button = button;
                    req_group = group;
                }
            });
        }
    }
    return [req_button, req_group];
}

function isInsideEquation(text, cursorPosition) {
    const stack = []; // Stack to keep track of opening characters ('$' or '$$')

    for (let i = 0; i < cursorPosition; i++) {
        if (text[i] === '$') {
            if (i > 0 && text[i - 1] === '$') {
                if (stack.length > 0 && stack[stack.length - 1] === '$$') {
                    stack.pop();
                } else {
                    stack.push('$$');
                }
            } else {
                stack.push('$');
            }
        }
    }
    return stack.length > 0;
}

function toolbarInsert(name) {
    const [button, group] = getButton(name);

    var textarea = document.querySelector('.rtxt-textarea');
    
    const equation_mode = isInsideEquation(textarea.value, textarea.selectionStart);

    if (button.cursor === 'end') {
        start_pos = end_pos = button.code.length;
    } else {
        [start_pos, end_pos] = button.cursor;
    }

    pre_text = textarea.value.slice(0, textarea.selectionStart);
    post_text = textarea.value.slice(textarea.selectionStart)
    
    start_pos = start_pos < 0 ? button.code.length + start_pos + 1 : start_pos;
    end_pos = end_pos < 0 ? button.code.length + end_pos + 1 : end_pos;
    start_pos += pre_text.length;
    end_pos += pre_text.length;
    
    if (group === 'image' || group === 'equation') {
        if (equation_mode) {
            console.log("Cannot insert this while enclosed in a latex equation!");
            textarea.focus();
            return;
        }
        else {
            code = button.code;
        }
    }
    else {
        if (equation_mode) {
            code = button.code;
        } else {
            code = '$'+button.code+'$'
            start_pos += 1;
            end_pos += 1;
        }
    }

    textarea.value = pre_text + code + post_text;
    textarea.focus();
    textarea.setSelectionRange(start_pos, end_pos);
}

var rich_textareas = document.querySelectorAll('div.rtxt');
rich_textareas.forEach(editor => {
    var toolbar = editor.querySelector('div.rtxt-toolbar');
    // var textarea = editor.querySelector('div.rtxt-textarea');

    var toolbar_code = '';
    for (const group in toolbar_buttons) {
        if (Object.hasOwnProperty.call(toolbar_buttons, group)) {
            var group_code = `<div class="btn-group me-2" role="group" aria-label="${group}">`;

            toolbar_buttons[group].forEach(button => {
                var button_code = `<button type="button" title="${button.description}" onclick="toolbarInsert('${button.name}')" class="btn btn-outline-secondary">${button.display}</button>`;
                group_code = group_code + button_code;
            });
            group_code = group_code + "</div>";
            toolbar_code = toolbar_code + group_code;
        }
    }

    toolbar.innerHTML = toolbar_code;
});