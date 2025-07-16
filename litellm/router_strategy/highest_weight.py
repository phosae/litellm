"""
Returns the deployment with the highest weight from the list of healthy deployments.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Union

from litellm._logging import verbose_router_logger

if TYPE_CHECKING:
    from litellm.router import Router as _Router

    LitellmRouter = _Router
else:
    LitellmRouter = Any


def highest_weight(
    llm_router_instance: LitellmRouter,
    healthy_deployments: Union[List[Any], Dict[Any, Any]],
    model: str,
) -> Dict[str, Any]:
    """
    Returns the deployment with the highest weight from the list of healthy deployments.
    
    If weights are provided, it will return a deployment with the highest weight.
    
    If all weights are zero, it will fall back to RPM-based selection.
    If all RPMs are zero, it will fall back to TPM-based selection.

    Args:
        llm_router_instance: LitellmRouter instance
        healthy_deployments: List of healthy deployments
        model: Model name

    Returns:
        Dict[str, Any]: A single healthy deployment
    """
    
    ############## Check if 'weight' param set for a weighted pick #################
    # Check if weights are available and not all zero
    weights = [d.get("litellm_params", {}).get("weight", 0) for d in healthy_deployments]
    if any(weight > 0 for weight in weights):
        # Find deployment with highest weight
        selected_deployment = max(healthy_deployments, key=lambda d: d.get("litellm_params", {}).get("weight", 0))
        verbose_router_logger.info(
            f"get_available_deployment for model: {model}, Selected deployment based on weight: {llm_router_instance.print_deployment(selected_deployment) or selected_deployment[0]} for model: {model}"
        )
        return selected_deployment or selected_deployment[0]
    
    ############## Check if we can do a RPM-based pick #################
    rpms = [d.get("litellm_params", {}).get("rpm", 0) for d in healthy_deployments]
    if any(rpm > 0 for rpm in rpms):
        # Find deployment with highest RPM
        selected_deployment = max(healthy_deployments, key=lambda d: d.get("litellm_params", {}).get("rpm", 0))
        verbose_router_logger.info(
            f"get_available_deployment for model: {model}, Selected deployment based on RPM: {llm_router_instance.print_deployment(selected_deployment) or selected_deployment[0]} for model: {model}"
        )
        return selected_deployment or selected_deployment[0]
    
    ############## Check if we can do a TPM-based pick #################
    tpms = [d.get("litellm_params", {}).get("tpm", 0) for d in healthy_deployments]
    if any(tpm > 0 for tpm in tpms):
        # Find deployment with highest TPM
        selected_deployment = max(healthy_deployments, key=lambda d: d.get("litellm_params", {}).get("tpm", 0))
        verbose_router_logger.info(
            f"get_available_deployment for model: {model}, Selected deployment based on TPM: {llm_router_instance.print_deployment(selected_deployment) or selected_deployment[0]} for model: {model}"
        )
        return selected_deployment or selected_deployment[0]
    
    ############## No weights, RPMs, or TPMs available, return first deployment #################
    selected_deployment = healthy_deployments[0]
    verbose_router_logger.info(
        f"get_available_deployment for model: {model}, No weights/RPMs/TPMs available, returning first deployment: {llm_router_instance.print_deployment(selected_deployment) or selected_deployment[0]} for model: {model}"
    )
    return selected_deployment or selected_deployment[0]
