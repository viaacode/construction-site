from collections import deque

import ijson
from rdflib import BNode, Literal, Namespace

def parse_json(json, namespace=Namespace("http://localhost/")):

    # initializing deque
    subjectStack = deque([])
    arrayProperties = {}
    property = None

    events = ijson.basic_parse(json, use_float = True)

    for event, value in events:
        if event == "start_array" and subjectStack and property is not None:
            # fetching the last subject
            s = subjectStack[-1]
            arrayProperties[s] = property

        if event == "end_array" and subjectStack:
            # fetching the last subject
            s = subjectStack[-1]
            arrayProperties.pop(s, None)

        if event == "start_map":
            subject = BNode()
            # add triple with current array property, if any
            if property is not None and subjectStack:
                # fetching the last subject
                s = subjectStack[-1]
                yield (s, property, subject)
            subjectStack.append(subject)

        if event == "end_map":
            subjectStack.pop()

            # restore previous array property, if there was any
            if subjectStack and subjectStack[-1] in arrayProperties:
                property = arrayProperties[subjectStack[-1]]

        if event in ["boolean", "integer", "double", "number"]:
            yield (subjectStack[-1], property, Literal(value))

        if event == "string" and property is not None:
            yield (subjectStack[-1], property, Literal(value))

        if event == "map_key":
            property = namespace[value]
