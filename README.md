# Simulator

This repository comprises several different types of simulators:

* [CounterIntervalSimulator](#counterintervalsimulator)
* [CounterSafeSimulator](#countersafesimulator)
* [IdentityIntervalSimulator](#identityintervalsimulator)
* [IdentityCronSimulator](#identitycronsimulator)
* [FileIntervalSimulator](#fileintervalsimulator)

##CounterIntervalSimulator


Notifies signals every interval.


##### Properties

-   **interval**: How often should the block notify signals
-   **total_signals**: The maximum number of signals to notify overall. If less than 0 (-1 by default), then the trigger will continue to notify indefinitely until the block is stopped.
   

##### Output
For a **CounterIntervalSimulator** with start=0, stop=12, step=3, and num_signals = 3, 
the output will be:
> **Note:** `*` is the point that the signals are notified

```
|------interval------|------interval------|------interval------|------interval------|
[ 0  3  6*             9 12  0*             3  6  9*            12  0  3*           ]
```

The **IntervalTrigger** operates in a single thread, so under heavy loads the interval 
will be ignored and signals will only be output as fast as they can.

For example, if num_signals = 14 from the above example, the output would look like:
> **Note:** `*` is the point that the signals are notified

> **Note:** Compare the below to the Output in **CounterSafeSimulator**

```
|------interval------|------interval------|------interval------|------interval------|
[ 0  3  6  9 12  0  3  6  9 12  0  3  6  9*12  0  3  6  9 12  0  3  6  9 12  0  3  6*]
```
In real-word applications this will happen at > 30,000 signals / second on most computers


##CounterSafeSimulator


Notify every interval - regardless of how many signals were created

***Does not support MultipleSignals***

##### Properties

-   **interval**: How often should the block notify signals
-   **max_count**: Maximum signals to notify — the block will never notify 
    more signals than this count every interval. However, if the number is too 
    high for it to create, it may return less than this number. The only 
    guarantee made by this block is that a notification will happen every 
    interval

##### Output
For a **CounterSafeSimulator** with `start=0, stop=12, step=3, and max_count = 3`
the output will be:
> **Note:** `*` is the point that the signals are notified

```
|------interval------|------interval------|------interval------|------interval------|
[ 0  3  6*             9 12  0*             3  6  9*            12  0  3*           ]
```

The **SafeTrigger** uses threading so that it can guarantee a notification every 
interval under heavy loads. 

For example, if `max_count == 14` from the above example, the output would look like:
> **Note:** `*` is the point that the signals are notified

> **Note:** Compare the below to the Output in **IdentityIntervalSimulator**

```
|------interval------|------interval------|------interval------|------interval------|
[ 0  3  6  9 12  0  3* 6  9 12  0  3  6  9*12  0  3  6  9 12  0* 3  6  9 12  0  3  6*]
```
In other words, if the simulator cannot reach `max_count` in the interval time, it will
notify anyways

In real-word applications this will happen at > 3,000 signals / second on most computers


##IdentityIntervalSimulator


Creates empty signals. This is most likely useful for driving some other type 
of Block that doesn't necessarily care about the signal contents, but rather 
that a signal has been notified.

##### Output
> **Note:** `{}` is an empty Signal object

```
[{} {} {} {} {} ...]
```


##IdentityCronSimulator


Creates empty signals. This is most likely useful for driving some other type 
of Block that doesn't necessarily care about the signal contents, but rather 
that a signal has been notified and the scheduling of that signal needs to be precise.

##### Output
> **Note:** `{}` is an empty Signal object

```
[{} {} {} {} {} ...]
```


##FileIntervalSimulator


Creates signals as defined by a json file. The file must be a list of dictionaries where each dictionary is a nio Signal. The file should be loadable using `json.load`.

Each call to generate_signals will return a signal from the list loaded in from the json file.

##### Properties

-   **signals_file**: The location of the file containing a list of signals. It can be an absolute file location, relative to the root project directory or relative to the block path.
-   **random_selection**: Whether or not to randomly pull from the file. If unchecked, the simulator will iterate through the file sequentially.

##### Output

Each output signal will be equivalent to a dictionary pulled in from the `signals_file`.
