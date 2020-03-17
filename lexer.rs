/*
Tokens are a struct which will always come like:
Token {
    name // The type of token this is, can only be one of the
        constants defined below.
    val // How it appears in your text file, unless specified otherwise
}
*/

const NUMBER: &'static str = "NUMBER";
const NAME: &'static str = "NAME";
// Val here is the line number it ends
const NEWLINE: &'static str = "NEWLINE";
// Val in the two below is how many spaces or tabs before the first token
const INDENT: &'static str = "INDENT";
const UNINDENT: &'static str = "UNINDENT";

const KEYWORD: &'static str = "KEYWORD";
// You won't find a Token.name = KEYWORDS, instead this one is used to identify keywords
// for Token.name = KEYWORD
const KEYWORDS: &[&'static str] = &["if", "let", "for"];

pub struct Token {
    name: &'static str,
    val: String,
}

impl Token {
    pub fn to_string(&self) -> String {
        format!("Token({}, {})", self.name, self.val)
    }
}

pub fn lexer(path: &str) -> Vec<Token> {
    fn is_number(ch: char) -> bool {
        return '0' <= ch && ch <= '9';
    }

    fn is_nam(ch: char) -> bool {
        return ('A' <= ch && ch <= 'Z') || ('a' <= ch && ch <= 'z') || (ch == '_');
    }

    fn check_indent(output: &mut Vec<Token>, spaces: u16) {
        for i in 0..output.len() {
            let j = output.len() - i - 1;
            match output.get(j) {
                Some(tkn) if tkn.name == INDENT || tkn.name == UNINDENT => {
                    let aux: u16 = tkn.val.parse::<u16>().unwrap();
                    if spaces > aux {
                        output.push(Token {
                            name: INDENT,
                            val: spaces.to_string(),
                        });
                    } else if spaces < aux {
                        output.push(Token {
                            name: UNINDENT,
                            val: spaces.to_string(),
                        });
                    }
                    return;
                }

                Some(_) | None => {}
            }
        }
    }

    let mut output = vec![Token {
        name: INDENT,
        val: "0".to_string(),
    }];
    let file = std::fs::read(path).expect(&format!("Unable to read file {}", path));
    let mut i: usize = 0;
    let mut ln: u128 = 1;
    let mut spaces: u16 = 0;
    loop {
        match file.get(i) {
            Some(byte) if is_number(*byte as char) => {
                check_indent(&mut output, spaces);
                let mut buffer = (*byte as char).to_string();
                loop {
                    match file.get(i + 1) {
                        Some(b) if is_number(*b as char) => {
                            buffer = format!("{}{}", buffer, *b as char);
                            i += 1;
                        }
                        Some(_) | None => break,
                    }
                }
                output.push(Token {
                    name: NUMBER,
                    val: buffer,
                });

                i += 1;
            }

            Some(byte) if is_nam(*byte as char) => {
                check_indent(&mut output, spaces);
                let mut buffer = (*byte as char).to_string();
                loop {
                    match file.get(i + 1) {
                        Some(b) if is_nam(*b as char) || is_number(*b as char) => {
                            buffer = format!("{}{}", buffer, *b as char);
                            i += 1;
                        }
                        Some(_) | None => break,
                    }
                }
                if KEYWORDS.iter().any(|&aux| aux == buffer) {
                    output.push(Token {
                        name: KEYWORD,
                        val: buffer,
                    });
                } else {
                    output.push(Token {
                        name: NAME,
                        val: buffer,
                    });
                }

                i += 1;
            }

            Some(byte) if *byte as char == '\n' => {
                check_indent(&mut output, spaces);
                output.push(Token {
                    name: NEWLINE,
                    val: ln.to_string(),
                });
                i += 1;
                ln += 1;
                spaces = 0;
            }

            Some(byte) if *byte == ' ' as u8 || *byte as char == '\t' => {
                match output.last() {
                    Some(tkn) if tkn.name == NEWLINE => {
                        spaces += 1;
                    }
                    Some(_) | None => {}
                }
                i += 1;
            }

            Some(_) => {
                i += 1;
            }
            None => (break),
        }
    }

    output.remove(0);
    return output;
}
