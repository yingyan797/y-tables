class Text:
    def __init__(self, content) -> None:
        self.content = content
        self.pos = 0

    def _end(self):
        return self.pos >= len(self.content)
    
    def _match(self, segs):
        for i in range(len(segs)):
            seg = segs[i]
            if self.content[self.pos:self.pos+len(seg)] == seg:
                self.pos += len(seg)
                return i
        return -1
    
    def read_tag(self, tags:str):
        istart = -1
        mtag = -1
        while not self._end():
            if istart < 0:
                mtag = self._match([f"<{tag}" for tag in tags])
                if mtag >= 0:
                    while self.content[self.pos] != ">":
                        self.pos += 1
                    istart = self.pos + 1
                else:
                    self.pos += 1
            else:
                if self._match([f"</{tags[mtag]}>"]) >= 0:
                    iend = self.pos-3-len(tags[mtag])
                    return self.content[istart:iend]
                self.pos += 1
            
def read_table(text):
    html = Text(text)
    table = []
    while True:
        tr = html.read_tag(["tr"])
        if tr is not None:
            row = Text(tr)
            read_row = []
            while True:
                td = row.read_tag(["td", "th"])
                if td is not None:
                    read_row.append(td)
                else:
                    break
            table.append(read_row)
        else:
            break
    return table
    
def entry_process(entry:str):
    segs = ["",""]
    i = 0
    for j in range(len(entry)):
        c = entry[j]
        if c == "]":
            i = 1
        elif c == "[":
            segs[i] = c+segs[i]
            segs[0] = entry[j+1:][::-1] + segs[0]
            break
        segs[i] = c + segs[i]
    
    words = []
    word = ""
    for c in segs[1]:
        if c.isalnum():
            word += c
        elif word:
            words.append(word)
            word = ""
    if word:
        words.append(word)

    return Text(segs[0]).read_tag("b"), words

def table_process(table:list[list[str]], kw=""):
    res, keys, kmax = [], [], []
    keywords = [k.lower() for k in kw.split(",")]
    # parse table
    for row in table:
        r = row[:3]
        title, heat = entry_process(row[3][::-1])
        tsq = title.lower() if title else ""
        switch = [False for _ in tsq]
        if tsq and keywords:
            for k in keywords:
                loc = tsq.find(k)
                if loc >= 0:
                    switch = switch[:loc] + [True for _ in k] + switch[loc+len(k):]
        segs = []
        prev, i = False, 0
        for j in range(len(switch)):
            if switch[j] != prev:
                segs.append((title[i:j], prev))
                i = j
                prev = switch[j]
        if j > i:
            segs.append((title[i:j], prev))

        r.append((len(segs) > 1, segs))
        if not keys:
            keys = [heat[i] for i in range(0, len(heat), 2)]
            kmax = [0 for _ in keys]
        ki = 0
        for i in range(1, len(heat), 2):
            v = int(heat[i])
            r.append([v,""])
            if v > kmax[ki]:
                kmax[ki] = v
            ki += 1
        nplace = ""
        for c in row[-2]:
            if not c.isalnum():
                break
            nplace += c
        r.append(int(nplace))
        res.append(r)
    
    # color gradient
    for row in res:
        for i in range(4, len(row)-1):
            color = hex(int(255 * (1- row[i][0]/kmax[i-4]))) if kmax[i-4] else "0xFF"
            row[i][1] = f"#{color[2:] if len(color) == 4 else '0'+color[2:]}FFFF"
    print(kmax)

    return keys, res
        
if __name__ == "__main__":
    # test
    with open("static/proposal.html") as f:
        text = f.read()
    table = read_table(text)
    print(table_process(table))
