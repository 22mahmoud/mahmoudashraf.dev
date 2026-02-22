from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import TYPE_CHECKING, Any

from pythonjsonlogger.json import JsonFormatter

if TYPE_CHECKING:
    from logging import LogRecord


def _first_forwarded_ip(value: Any) -> str | None:
    if value is None:
        return None

    ip_value = str(value).strip()
    if not ip_value or ip_value == "-":
        return None

    first_ip = ip_value.split(",", 1)[0].strip()
    if not first_ip or first_ip == "-":
        return None

    return first_ip


class DjangoJsonRequestFormatter(JsonFormatter):
    def add_fields(
        self,
        log_data: dict[str, Any],
        record: LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_data, record, message_dict)

        log_data["time"] = datetime.fromtimestamp(record.created).isoformat()
        log_data.pop("asctime", None)

        log_data.update(
            {
                "pid": record.process,
                "thread": record.thread,
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
                "message": record.getMessage(),
            }
        )


class JsonRequestFormatter(JsonFormatter):
    def add_fields(
        self,
        log_data: dict[str, Any],
        record: LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        args: Mapping[str, Any] = record.args if isinstance(record.args, Mapping) else {}

        t = args.get("t", "").strip("[]")
        response_time = None

        if t:
            try:
                response_time = datetime.strptime(t, "%d/%b/%Y:%H:%M:%S %z")
            except ValueError as e:
                print(f"Failed to parse timestamp '{t}': {e}")

        url = args.get("U", "")
        if args.get("q"):
            url += f"?{args['q']}"

        remote_ip = (
            _first_forwarded_ip(args.get("{cf-connecting-ip}i"))
            or _first_forwarded_ip(args.get("{x-forwarded-for}i"))
            or _first_forwarded_ip(args.get("{x-real-ip}i"))
            or _first_forwarded_ip(args.get("h"))
        )

        log_data.update(
            {
                "remote_ip": remote_ip,
                "method": args.get("m"),
                "path": url,
                "status": args.get("s"),
                "time": response_time.isoformat() if response_time else None,
                "user_agent": args.get("a"),
                "referer": args.get("f"),
                "duration_in_ms": args.get("M"),
                "pid": args.get("p"),
            }
        )


class JsonErrorFormatter(JsonFormatter):
    def add_fields(
        self,
        log_data: dict[str, Any],
        record: LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_data, record, message_dict)
        log_data["level"] = log_data.get("levelname", "")
