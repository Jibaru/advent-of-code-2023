from math import lcm

'''
--- Day 20: Pulse Propagation ---
With your help, the Elves manage to find the right parts and fix all of the machines. Now, they just need to send the command to boot up the machines and get the sand flowing again.

The machines are far apart and wired together with long cables. The cables don't connect to the machines directly, but rather to communication modules attached to the machines that perform various initialization tasks and also act as communication relays.

Modules communicate using pulses. Each pulse is either a high pulse or a low pulse. When a module sends a pulse, it sends that type of pulse to each module in its list of destination modules.

There are several different types of modules:

Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.

Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.

There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.

Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly, the button module. When you push the button, a single low pulse is sent directly to the broadcaster module.

After pushing the button, you must wait until all pulses have been delivered and fully handled before pushing it again. Never push the button if modules are still processing pulses.

Pulses are always processed in the order they are sent. So, if a pulse is sent to modules a, b, and c, and then module a processes its pulse and sends more pulses, the pulses sent to modules b and c would have to be handled first.

The module configuration (your puzzle input) lists each module. The name of the module is preceded by a symbol identifying its type, if any. The name is then followed by an arrow and a list of its destination modules. For example:

broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
In this module configuration, the broadcaster has three destination modules named a, b, and c. Each of these modules is a flip-flop module (as indicated by the % prefix). a outputs to b which outputs to c which outputs to another module named inv. inv is a conjunction module (as indicated by the & prefix) which, because it has only one input, acts like an inverter (it sends the opposite of the pulse type it receives); it outputs to a.

By pushing the button once, the following pulses are sent:

button -low-> broadcaster
broadcaster -low-> a
broadcaster -low-> b
broadcaster -low-> c
a -high-> b
b -high-> c
c -high-> inv
inv -low-> a
a -low-> b
b -low-> c
c -low-> inv
inv -high-> a
After this sequence, the flip-flop modules all end up off, so pushing the button again repeats the same sequence.

Here's a more interesting example:

broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
This module configuration includes the broadcaster, two flip-flops (named a and b), a single-input conjunction module (inv), a multi-input conjunction module (con), and an untyped module named output (for testing purposes). The multi-input conjunction module con watches the two flip-flop modules and, if they're both on, sends a low pulse to the output module.

Here's what happens if you push the button once:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -high-> output
b -high-> con
con -low-> output
Both flip-flops turn on and a low pulse is sent to output! However, now that both flip-flops are on and con remembers a high pulse from each of its two inputs, pushing the button a second time does something different:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
Flip-flop a turns off! Now, con remembers a low pulse from module a, and so it sends only a high pulse to output.

Push the button a third time:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -low-> output
b -low-> con
con -high-> output
This time, flip-flop a turns on, then flip-flop b turns off. However, before b can turn off, the pulse sent to con is handled first, so it briefly remembers all high pulses for its inputs and sends a low pulse to output. After that, flip-flop b turns off, which causes con to update its state and send a high pulse to output.

Finally, with a on and b off, push the button a fourth time:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
This completes the cycle: a turns off, causing con to remember only low pulses and restoring all modules to their original states.

To get the cables warmed up, the Elves have pushed the button 1000 times. How many pulses got sent as a result (including the pulses sent by the button itself)?

In the first example, the same thing happens every time the button is pushed: 8 low pulses and 4 high pulses are sent. So, after pushing the button 1000 times, 8000 low pulses and 4000 high pulses are sent. Multiplying these together gives 32000000.

In the second example, after pushing the button 1000 times, 4250 low pulses and 2750 high pulses are sent. Multiplying these together gives 11687500.

Consult your module configuration; determine the number of low pulses and high pulses that would be sent after pushing the button 1000 times, waiting for all pulses to be fully handled after each push of the button. What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?

Your puzzle answer was 879834312.
'''

HIGH_PULSE = True
LOW_PULSE = False

ON_STATE = True
OFF_STATE = False

class Module:
    def __init__(self, name: str, destinations: list[str]) -> None:
        self.name = name
        self.destinations = destinations

class FlipFlop(Module):
    def __init__(self, name: str, destinations: list[str], state: bool = False) -> None:
        super().__init__(name, destinations)
        self.state = state

    def is_on(self) -> bool:
        return self.state == ON_STATE

    def is_off(self) -> bool:
        return self.state == OFF_STATE

    def turn_off(self):
        self.state = OFF_STATE

    def turn_on(self):
        self.state = ON_STATE

    def __repr__(self) -> str:
        return f'F({self.name}, {self.destinations}, {self.state})'

class Conjuction(Module):
    def __init__(self, name: str, destinations: list[str], last_pulses: dict[str, bool]) -> None:
        super().__init__(name, destinations)
        self.last_pulses = last_pulses

    def update_memory(self, name: str, pulse: bool):
        self.last_pulses[name] = pulse

    def next_pulse(self) -> bool:
        pulses = set(self.last_pulses.values())
        if len(pulses) == 1 and HIGH_PULSE in pulses:
            return LOW_PULSE
        return HIGH_PULSE

    def __repr__(self) -> str:
        return f'C({self.name}, {self.destinations}, {self.last_pulses})'

class Broadcaster(Module):
    def __init__(self, name: str, destinations: list[str]) -> None:
        super().__init__(name, destinations)

    def __repr__(self) -> str:
        return f'B({self.name}, {self.destinations})'

def process_module(
    module: Module,
    from_name: str,
    pulse: bool,
    queue: list[(str, str, bool)],
    on_conjunction = None
):    
    if isinstance(module, FlipFlop):
        if pulse == LOW_PULSE:
            if module.is_on():
                module.turn_off()
                for destination in module.destinations:
                    queue.append((module.name, destination, LOW_PULSE))
            else:
                module.turn_on()
                for destination in module.destinations:
                    queue.append((module.name, destination, HIGH_PULSE))
    elif isinstance(module, Conjuction):
        module.update_memory(from_name, pulse)
        next_pulse = module.next_pulse()
        
        if on_conjunction != None:
            on_conjunction(module.name, next_pulse)
        
        for destination in module.destinations:
            queue.append((module.name, destination, next_pulse))
    elif isinstance(module, Broadcaster):
        for destination in module.destinations:
            queue.append((module.name, destination, pulse))

def parse_modules(data: str) -> map:
    modules: map[str, Module] = {}

    for line in data.split('\n'):
        name, destinations = line.split(' -> ')
        destinations = destinations.split(', ')

        if '%' in name:
            modules[name[1:]] = FlipFlop(name[1:], destinations)
        elif '&' in name:
            modules[name[1:]] = Conjuction(name[1:], destinations, {})
        else:
            modules[name] = Broadcaster(name, destinations)

    for name in modules:
        for destination in modules[name].destinations:
            if destination in modules and isinstance(modules[destination], Conjuction):
                modules[destination].update_memory(name, LOW_PULSE)

    return modules

def solve01(data: str):
    modules = parse_modules(data)

    total_pulses = {
        HIGH_PULSE: 0,
        LOW_PULSE: 0,
    }

    for _ in range(1000):
        queue = []
        queue.append(('.', 'broadcaster', LOW_PULSE))

        while queue:
            from_name, to_name, pulse = queue.pop(0)

            total_pulses[pulse] += 1

            if to_name not in modules:
                continue

            process_module(modules[to_name], from_name, pulse, queue)

    return total_pulses[HIGH_PULSE] * total_pulses[LOW_PULSE]

'''
--- Part Two ---
The final machine responsible for moving the sand down to Island Island has a module attached named rx. The machine turns on when a single low pulse is sent to rx.

Reset all modules to their default states. Waiting for all pulses to be fully handled after each button press, what is the fewest number of button presses required to deliver a single low pulse to the module named rx?

Your puzzle answer was 243037165713371.
'''

def solve02(data: str):
    modules = parse_modules(data)

    conjunctions_need_to_be_high_pulsed = {
        'mr': [-1, False],
        'kk': [-1, False],
        'bb': [-1, False],
        'gl': [-1, False],
    }
    times_pressed = 1
    values = None

    def on_conjunction(name: str, pulse: bool):
        if name in conjunctions_need_to_be_high_pulsed and pulse == HIGH_PULSE:
            conjunctions_need_to_be_high_pulsed[name] = [times_pressed, pulse]

    while values is None:
        queue = []
        queue.append(('.', 'broadcaster', LOW_PULSE))
        
        while queue:
            from_name, to_name, pulse = queue.pop(0)
    
            if to_name not in modules:
                continue

            process_module(modules[to_name], from_name, pulse, queue, on_conjunction)

            if False not in set([i[1] for i in conjunctions_need_to_be_high_pulsed.values()]):
                values = [i[0] for i in conjunctions_need_to_be_high_pulsed.values()]

        times_pressed += 1

    return lcm(*values)

if __name__ == "__main__":
    # data = open('day-20-input.test.txt', 'r').read()
    data = open('day-20-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
