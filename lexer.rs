const NUM: &str = "NUM";
const NAME: &str = "NAME";
const NL: &str = "NL";
const KW: &str = "KW";

const KEYWORDS: [&str; 2] = ["if", "for"];

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

    let mut output: Vec<Token> = Vec::new();
    let file = std::fs::read(path).expect(&format!("Unable to read file {}", path));
    let mut i: usize = 0; let mut ln: u128 = 1;
    loop {
        match file.get(i) {
            Some(byte) if is_number(*byte as char) => {
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
                output.push(Token {name: NL, val: ln.to_string()});
                i+=1; ln+=1;
            }

            Some(_) => {i+=1;}
            None => (break)
        }
    }

    return output;
}
