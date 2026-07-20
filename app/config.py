"""
Project X - Configuration System

This file contains the basic configuration
of the Project X AI system.
"""

PROJECT_NAME = "Project X"
PROJECT_VERSION = "1.0.0"

ENVIRONMENT = "development"

AI_SYSTEM_STATUS = "active"


def get_config():
    """
    Returns Project X configuration.
    """

    return {
        "project_name": PROJECT_NAME,
        "version": PROJECT_VERSION,
        "environment": ENVIRONMENT,
        "status": AI_SYSTEM_STATUS
    }
