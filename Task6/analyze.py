import argparse
import json
import sys

from datetime import datetime, timezone

def parse_json_file(file_path, from_string):
    try:
        stats = {}

        log = {}

        from_ = datetime.strptime(from_string, "%Y-%m-%dT%H:%M:%S.%f%z")

        with open(file_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if 'audit.k8s.io/v1' not in line:
                    continue

                try:
                    event = json.loads(line)

                    audit_id = event.get('auditID', None)

                    if audit_id is not None:
                        stage = event.get('stage', None)

                        if stage == 'ResponseComplete':
                            user = event.get('user', {}).get('username', None)

                            impersonated_user = event.get('impersonatedUser', {}).get('username', None)

                            verb = event.get('verb', None)

                            object = event.get('objectRef', {})

                            resource = object.get('resource', None)

                            subresource = object.get('subresource', None)

                            namespace = object.get('namespace', None)

                            annotations = event.get('annotations', {})

                            decision = annotations.get('authorization.k8s.io/decision', None)

                            at_string = event.get('requestReceivedTimestamp', None)

                            at = datetime.strptime(at_string, "%Y-%m-%dT%H:%M:%S.%f%z")

                            if at > from_:
                                event_string = f"user {user if impersonated_user is None else impersonated_user} was {'ALLOWED' if decision == 'allow' else 'FORBIDDEN'} to {verb} {resource}{'' if subresource is None else '/' + subresource} in {namespace} namespace"

                                stats[event_string] = stats.get(event_string, 0) + 1

                                # Do something with your JSON object here
                                print(f"[{at_string}] {event_string}")

                except json.JSONDecodeError as e:
                    print(
                        f"Error parsing JSON on line {line_number}: {e}",
                        file=sys.stderr,
                    )

        print()

        for event_string, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
            print(f"{event_string} {count} times")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(
            f"Error: Permission denied to read '{file_path}'.", file=sys.stderr
        )
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze k8s audit logs."
    )

    parser.add_argument(
        "filename", help="Path to k8s audit.log file."
    )

    parser.add_argument(
        "from", help="Timestamp that events are taken from, in '%Y-%m-%dT%H:%M:%S.%f%z' format."
    )

    args = parser.parse_args()

    parse_json_file(args.filename, getattr(args, 'from'))


if __name__ == "__main__":
    main()

