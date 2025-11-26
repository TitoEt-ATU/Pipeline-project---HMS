"""
Datadog Configuration for Hospital Management System
Enables APM (Application Performance Monitoring), logging, and metrics
"""

import os
from ddtrace import config, tracer, patch_all
from ddtrace.profiling import profiler

# Initialize Datadog tracing
def init_datadog():
    """Initialize Datadog APM and monitoring"""
    
    # Check if Datadog is enabled
    datadog_enabled = os.getenv('DATADOG_ENABLED', 'true').lower() == 'true'
    
    if not datadog_enabled:
        print("⚠️  Datadog monitoring is disabled")
        return
    
    # Get Datadog configuration
    env = os.getenv('DATADOG_ENV', 'production')
    service = os.getenv('DATADOG_SERVICE_NAME', 'hms-app')
    version = os.getenv('DATADOG_VERSION', 'unknown')
    
    try:
        # Auto patch supported integrations
        patch_all()
        # Ensure tracer is enabled
        tracer.enabled = True
        
        # Configure service info
        config.service = service
        config.env = env
        config.version = version
        
        # Enable Flask integration
        config.flask['trace_render_view'] = True
        config.flask['trace_abort_handler'] = True
        
        # Enable SQLAlchemy integration for database tracing
        if hasattr(config, 'sqlalchemy'):
            config.sqlalchemy['trace_rows_per_cursor'] = True
        
        # Configure profiler (guarded; some ddtrace versions may not expose profiler.start)
        try:
            if hasattr(profiler, 'start'):
                profiler.start(
                    service=service,
                    env=env,
                    version=version,
                    tags={
                        'service': service,
                        'env': env,
                        'version': version,
                    }
                )
            else:
                print('⚠️  Datadog profiler API (profiler.start) is not available in this ddtrace version; skipping profiler start.')
        except Exception as e:
            print(f'⚠️  Datadog profiler failed to start: {e}')
        
        print(f"✅ Datadog APM initialized - Service: {service}, Env: {env}, Version: {version}")
        return True
        
    except Exception as e:
        print(f"⚠️  Failed to initialize Datadog: {str(e)}")
        return False


def configure_datadog_logging():
    """Configure Datadog JSON logging"""
    import logging
    from datadog.api import EnvironmentBase
    
    # Set up structured logging for Datadog
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'stream': 'ext://sys.stdout',
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    }
    
    return logging_config


# Datadog custom metrics
class DatadogMetrics:
    """Helper class for sending custom metrics to Datadog"""
    
    @staticmethod
    def increment_metric(metric_name: str, value: int = 1, tags: dict = None):
        """Increment a metric"""
        try:
            from datadog.api import api
            if tags is None:
                tags = {}
            api.Metric.send(
                metric=f"hms.{metric_name}",
                points=value,
                tags=[f"{k}:{v}" for k, v in tags.items()]
            )
        except Exception as e:
            print(f"⚠️  Failed to send metric: {str(e)}")
    
    @staticmethod
    def gauge_metric(metric_name: str, value: float, tags: dict = None):
        """Set a gauge metric"""
        try:
            from datadog.api import api
            if tags is None:
                tags = {}
            api.Metric.send(
                metric=f"hms.{metric_name}",
                points=value,
                metric_type='gauge',
                tags=[f"{k}:{v}" for k, v in tags.items()]
            )
        except Exception as e:
            print(f"⚠️  Failed to send gauge metric: {str(e)}")


# Export initialization functions
__all__ = ['init_datadog', 'configure_datadog_logging', 'DatadogMetrics']
