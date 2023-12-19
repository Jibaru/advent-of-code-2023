import re

'''
--- Day 19: Aplenty ---
The Elves of Gear Island are thankful for your help and send you on your way. They even have a hang glider that someone stole from Desert Island; since you're already going that direction, it would help them a lot if you would use it to get down there and return it to them.

As you reach the bottom of the relentless avalanche of machine parts, you discover that they're already forming a formidable heap. Don't worry, though - a group of Elves is already here organizing the parts, and they have a system.

To start, each part is rated in each of four categories:

x: Extremely cool looking
m: Musical (it makes a noise when you hit it)
a: Aerodynamic
s: Shiny
Then, each part is sent through a series of workflows that will ultimately accept or reject the part. Each workflow has a name and contains a list of rules; each rule specifies a condition and where to send the part if the condition is true. The first rule that matches the part being considered is applied immediately, and the part moves on to the destination described by the rule. (The last rule in each workflow has no condition and always applies if reached.)

Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}. This workflow is named ex and contains four rules. If workflow ex were considering a specific part, it would perform the following steps in order:

Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named one.
Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the workflow named two.
Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately rejected (R).
Rule "A": Otherwise, because no other rules matched the part, the part is immediately accepted (A).
If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns. If a part is accepted (sent to A) or rejected (sent to R), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes. The Elves ask if you can help sort a few parts and give you the list of workflows and some part ratings (your puzzle input). For example:

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to sort. All parts begin in the workflow named in. In this example, the five listed parts go through the following workflows:

{x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
{x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
{x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
{x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
{x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A
Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of the accepted parts gives 7540 for the part with x=787, 4623 for the part with x=2036, and 6951 for the part with x=2127. Adding all of the ratings for all of the accepted parts gives the sum total of 19114.

Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all of the parts that ultimately get accepted?

Your puzzle answer was 434147.
'''

def parse_rule(rule: str) -> str:
    pattern = re.compile(r'([a-z]+)(<|>)(\d+):([a-zA-Z]+)')
    match = pattern.match(rule)
    if match:
        groups = match.groups()
        return groups

    return None

def evaluator(rule, rating) -> str:
    if '<' in rule or '>' in rule:
        letter, operator, val, to = parse_rule(rule)
        val = int(val)
        if '<' == operator:
            return to if rating[letter] < val else ''
        if '>' == operator:
            return to if rating[letter] > val else ''

    return rule

def parse_workflows(data: str):
    workflows = {}
    
    for line in data.split('\n'):
        name, rules = line.split('{')
        rules = rules[:-1].split(',')
        workflows[name] = rules

    return workflows

def parse_ratings(data: str) -> int:
    ratings = []
    pattern = re.compile(r'(\w)=(\d+)')
    for line in data.split('\n'):
        matches = pattern.findall(line)
        rating = dict(matches)
        rating = {key: int(value) for key, value in matches}
        ratings.append(rating)
    
    return ratings

def solve01(data: str):
    workflow_data, ratings_data = data.split('\n\n')

    workflows = parse_workflows(workflow_data)
    ratings = parse_ratings(ratings_data)

    ans = 0
    STOP_WORKFLOW_NAMES = ['A', 'R']

    for rating in ratings:
        current_workflow = 'in'

        while current_workflow not in STOP_WORKFLOW_NAMES:
            for rule in workflows[current_workflow]:
                res = evaluator(rule, rating)

                if res == '':
                    continue

                current_workflow = res
                break

        if current_workflow == 'A':
            ans += sum(rating.values())

    return ans

'''
--- Part Two ---
Even with your help, the sorting process still isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, maybe you can figure out in advance which combinations of ratings will be accepted or rejected.

Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1 to a maximum of 4000. Of all possible distinct combinations of ratings, your job is to figure out which ones will be accepted.

In the above example, there are 167409079868000 distinct combinations of ratings that will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant. How many distinct combinations of ratings will be accepted by the Elves' workflows?

Your puzzle answer was 136146366355609.
'''

class Range:
    def __init__(self, start = None, stop = None):
        self.start = start
        self.stop = stop

    def is_empty(self) -> bool:
        return self.start == None or self.stop == None

    def is_not_empty(self) -> bool:
        return not self.is_empty()

    def intersect(self, other):
        if self.is_empty() or other.is_empty():
            return Range()

        if self.stop < other.start or self.start > other.stop:
            return None

        start = max(self.start, other.start)
        end = min(self.stop, other.stop)

        return Range(
            min(start, end),
            max(start, end)
        )
    
    def size(self) -> int:
        return self.stop - self.start + 1

    def copy(self):
        return Range(self.start, self.stop)

    def __str__(self) -> str:
        return f"({self.start}, {self.stop})"
    
    def __repr__(self) -> str:
        return self.__str__()


def copy_rating(rating: dict[str, Range]) -> dict[str, Range]:
    return {
        'x': rating['x'].copy(),
        'm': rating['m'].copy(),
        'a': rating['a'].copy(),
        's': rating['s'].copy(),
    }

def generate_ranges(operator: str, value: int) -> tuple[Range, Range]:
    if operator == '<':
        return (Range(1, value - 1), Range(value, 4000))
    elif operator == '>':
        return (Range(value + 1, 4000), Range(1, value))

    return (None, None)

def sum_possible_values(rating: dict[str, Range]) -> int:
    return rating['x'].size() * rating['m'].size() * rating['a'].size() * rating['s'].size()

def solve02(data: str) -> int:
    workflows_data, _ = data.split('\n\n')
    workflows = parse_workflows(workflows_data)

    ratings = [{
        'workflow': 'in',
        'rule': 0,
        'rating': {
            'x': Range(1, 4000),
            'm': Range(1, 4000),
            'a': Range(1, 4000),
            's': Range(1, 4000)
        },
    }]

    ans = 0

    while len(ratings) > 0:
        info = ratings.pop(0)

        name = info['workflow']
        rule_idx = info['rule']
        rating = info['rating']

        if name == 'A':
            ans += sum_possible_values(rating)
            continue
        
        if name == 'R':
            continue
        
        rule = workflows[name][rule_idx]
        
        if rule == 'R':
            continue
        
        if rule == 'A':
            ans += sum_possible_values(rating)
            continue

        if '<' in rule or '>' in rule:
            letter, operator, n, to = parse_rule(rule)
            n = int(n)

            left, right = generate_ranges(operator, n)
            
            new_rating = copy_rating(rating)
            new_range = new_rating[letter].intersect(left)
            if new_range.is_not_empty():
                new_rating[letter] = new_range
                
                ratings.append({
                    'workflow': to,
                    'rule': 0,
                    'rating': new_rating
                })

            new_rating = copy_rating(rating)
            new_range = new_rating[letter].intersect(right)
            if new_range.is_not_empty():
                new_rating[letter] = new_range
                ratings.append({
                    'workflow': name,
                    'rule': rule_idx + 1,
                    'rating': new_rating
                })
        else:
            ratings.append({
                'workflow': rule,
                'rule': 0,
                'rating': copy_rating(rating)
            })

    return ans

if __name__ == "__main__":
    # data = open('day-19-input.test.txt', 'r').read()
    data = open('day-19-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
