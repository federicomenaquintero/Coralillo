const NAME: &str = "NAME";
const NUMBER: &str = "NUMBER";
const INDENT: &str = "INDENT";
const UNINDENT: &str = "UNINDENT";
const NWLN: &str = "NWLN";
const KEYWORD: &str = "KEYWORD";
const KEYWORDS: [&str; 3] = ["if", "else", "for"];

pub struct Token {
    name: &'static str,
    value: String,
}
impl Token {
    pub fn new(name: &'static str, value: String) -> Token {
        Token { name, value }
    }
}

pub fn lexer(file: Vec<u8>) -> Result<Vec<Token>, String> {
    let mut _aux = Vec::<char>::new();
    let file_slice: &[char] = {
        for byte in file {
            _aux.push(byte as char)
        }
        _aux.as_ref()
    };
    let _aux = 0;

    let mut output = Vec::<Token>::new();
    let mut i: usize = 0;
    let mut line_counter = 0_u128;
    let mut ind_counter = 0_u16;
    let mut last_ind = 0_u16;
    while i < file_slice.len() {
        // Indentation
        if let Some(tkn) = output.last() {
            if tkn.name == NWLN {
                if file_slice[i] == ' ' || file_slice[i] == '\t' {
                    ind_counter += 1;
                    i += 1;
                    continue;
                } else {
                    use std::cmp::Ordering::*;
                    match ind_counter.cmp(&last_ind) {
                        Greater => output.push(Token::new(INDENT, ind_counter.to_string())),
                        Less => output.push(Token::new(UNINDENT, ind_counter.to_string())),
                        Equal => {}
                    }
                    last_ind = ind_counter;
                    ind_counter = 0;
                }
            }
        }

        // Names and keywords
        if file_slice[i].is_alphabetic() {
            let mut value = String::new();
            while file_slice[i].is_alphanumeric() {
                value.push(file_slice[i]);
                i += 1
            }

            if KEYWORDS.contains(&value.as_str()) {
                output.push(Token::new(KEYWORD, value))
            } else {
                output.push(Token::new(NAME, value))
            }
        }

        // Numbers
        if file_slice[i].is_digit(10) {
            let mut value = String::new();
            while file_slice[i].is_digit(10) {
                value.push(file_slice[i]);
                i += 1
            }

            output.push(Token::new(NUMBER, value))
        }

        // Single character tokens
        match file_slice[i] {
            '\r' | ' ' | '\t' => {}
            '\n' => {
                line_counter += 1;
                output.push(Token::new(NWLN, line_counter.to_string()))
            }
            unexpected => return Err(format!("Lexer Error: Unexpected Token {}", unexpected)),
        }

        i += 1
    }

    Ok(output)
}
