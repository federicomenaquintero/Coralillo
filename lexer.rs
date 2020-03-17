const NUM: &str = "NUM";
const NAME: &str = "NAME";
const NL: &str = "NL";
const KW: &str = "KW";
const IND: &str = "IND";
const UIND: &str = "UIND";

const KEYWORDS: [&str; 3] = ["if", "let", "for"];

pub struct Token<'a> {
    name: &'a str,
    val: String,
}

impl Token<'_> {
    pub fn to_string(&self) -> String {
        format!("Token({}, {})", self.name, self.val)
    }
}

pub fn lexer (path: &str) -> Vec<Token> {
    fn is_number(ch: char) -> bool {
        return '0' <= ch && ch <= '9';
    }

    fn is_nam(ch: char) -> bool {
        return ('A' <= ch && ch <= 'Z') ||
               ('a' <= ch && ch <= 'z') ||
               (ch  == '_')
    }

    fn check_indent(output: &mut Vec<Token>, spaces: u16) {
        for i in 0..output.len() {
            let j = output.len()-i-1;
            match output.get(j) {
                Some(tkn) if tkn.name == IND || tkn.name == UIND => {
                    let aux: u16 = tkn.val.parse::<u16>().unwrap();
                    if spaces > aux {
                        output.push(Token {name: IND, val: spaces.to_string()});
                    }
                    else if spaces < aux {
                        output.push(Token {name: UIND, val: spaces.to_string()});
                    }
                    return;
                } 

                Some(_) | None => {}
            }
        }
    }

    let mut output = vec![Token {name: IND, val: "0".to_string()}];
    let file = std::fs::read(path).expect(&format!("Unable to read file {}", path));
    let mut i: usize = 0; let mut ln: u128 = 1; let mut spaces: u16 = 0;
    loop {
        match file.get(i) {
            Some(byte) if is_number(*byte as char) => {
                check_indent(&mut output, spaces);
                let mut buffer = (*byte as char).to_string();
                loop {
                    match file.get(i+1) {
                        Some(b) if is_number(*b as char) => {
                            buffer = format!("{}{}", buffer, *b as char);
                            i+=1;
                        }
                        Some(_) | None => {break}
                    }
                }
                output.push(Token {name: NUM, val: buffer});

                i+=1;
            }

            Some(byte) if is_nam(*byte as char) => {
                check_indent(&mut output, spaces);
                let mut buffer = (*byte as char).to_string();
                loop {
                    match file.get(i+1) {
                        Some(b) if is_nam(*b as char) || is_number(*b as char) => {
                            buffer = format!("{}{}", buffer, *b as char);
                            i+=1;
                        }
                        Some(_) | None => {break}
                    }
                }
                if KEYWORDS.iter().any(|&aux| aux == buffer) {
                    output.push(Token {name: KW, val: buffer});
                }
                else {
                    output.push(Token {name: NAME, val: buffer});
                }

                i+=1;
            }

            Some(byte) if *byte as char == '\n' => {
                check_indent(&mut output, spaces);
                output.push(Token {name: NL, val: ln.to_string()});
                i+=1; ln+=1; spaces = 0;
            }

            Some(byte) if *byte == ' ' as u8 || *byte as char == '\t' => {
                match output.last() {
                    Some(tkn) if tkn.name == NL => {
                        spaces += 1;
                    }
                    Some(_) | None => {}
                }
                i+=1;
            }

            Some(_) => {i+=1;}
            None => (break)
        }
    }

    output.remove(0);
    return output;
}
