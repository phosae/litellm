import httpx
from litellm.integrations.custom_logger import CustomLogger
from typing import Optional, Union, Any
from litellm.types.router import ModelResponse
from litellm.exceptions import BadRequestError, RateLimitError # Import relevant LiteLLM exceptions
import litellm

# This file includes the custom callbacks for LiteLLM Proxy
# Once defined, these can be passed in proxy_config.yaml
class MyCustomHandler(CustomLogger):
    def log_pre_api_call(self, model, messages, kwargs): 
        print(f"Pre-API Call")
    
    def log_post_api_call(self, kwargs, response_obj, start_time, end_time): 
        print(f"Post-API Call")
        
    def log_success_event(self, kwargs, response_obj, start_time, end_time): 
        print("On Success")
        
    def log_failure_event(self, kwargs, response_obj, start_time, end_time): 
        print(f"On Failure")

    # async def log_failure_event(
    #     self,
    #     model: str,
    #     messages: list,
    #     response: Optional[Union[ModelResponse, str]], # response can be ModelResponse or an error string
    #     start_time: float,
    #     end_time: float,
    #     api_key: Optional[str] = None,
    #     caching_only: Optional[bool] = False,
    #     extra_body: Optional[dict] = None,
    #     exception: Optional[Exception] = None,
    #     # The crucial part: raw_response is often available for HTTP details
    #     raw_response: Optional[Any] = None # This is usually the httpx.Response object
    # ):
    #     """
    #     This hook is called when a LiteLLM call fails.
    #     We check if the failure was due to an HTTP 400 response.
    #     """
    #     if raw_response is not None:
    #         # Check if raw_response is an HTTPX Response object and if its status code is 400
    #         # You might need to import httpx to check the type if doing robust type checking
    #         # from httpx import Response as HTTPXResponse
    #         # if isinstance(raw_response, HTTPXResponse) and raw_response.status_code == 400:

    #         # Simple check for status_code attribute
    #         if hasattr(raw_response, 'status_code') and raw_response.status_code == 400:
    #             print(f"Detected 400 error from upstream model {model}. Initiating cooldown manually.")
    #         # LiteLLM's internal cooldown mechanism is triggered by marking the model as a failure.
    #         # When this hook returns, if it's considered a failure, LiteLLM's router will
    #         # increment `allowed_fails` count for this model and potentially put it in cooldown.
    #         # So, simply logging it here with this hook's context *should* be enough
    #         # IF LiteLLM passes enough context for it to be treated as a failure.

    #         # If this doesn't automatically trigger LiteLLM's cooldown (which it should,
    #         # as this is a log_failure_event), you might need more advanced control.
    #         # For example, if you wanted to explicitly manipulate LiteLLM's router state,
    #         # which would involve accessing the router object, it's complex and not
    #         # exposed via simple hooks.

    #         # However, this `log_failure_event` is designed for failures. If LiteLLM
    #         # internally passes a 400 as an 'exception' or a 'failure response',
    #         # this hook will be called and LiteLLM's router should then process it
    #         # according to its `allowed_fails` and `cooldown_time`.

    #         # You don't return anything from this hook, it's for logging/side effects.
    #         # LiteLLM already knows it's a failure because this hook was called.
    #             pass
    #         else:
    #             print(f"Log failure event for {model}, but not a 400 error. Status: {getattr(raw_response, 'status_code', 'N/A')}")
    #     else:
    #         print(f"Log failure event for {model}, no raw_response available.")

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        print(f"On Async Success!")
        # log: key, user, model, prompt, response, tokens, cost
        # Access kwargs passed to litellm.completion()
        model = kwargs.get("model", None)
        messages = kwargs.get("messages", None)
        user = kwargs.get("user", None)

        # Access litellm_params passed to litellm.completion(), example access `metadata`
        litellm_params = kwargs.get("litellm_params", {})
        metadata = litellm_params.get("metadata", {})   # headers passed to LiteLLM proxy, can be found here

        # Calculate cost using  litellm.completion_cost()
        cost = litellm.completion_cost(completion_response=response_obj)
        response = response_obj
        # tokens used in response 
        usage = response_obj["usage"]

        print(
            f"""
                Model: {model},
                Messages: {messages},
                User: {user},
                Usage: {usage},
                Cost: {cost},
                Response: {response}
                Proxy Metadata: {metadata}
            """
        )
        return

    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time): 
        model = kwargs.get("model") # Get model name from kwargs
        raw_response = kwargs.get("raw_response") # Get raw_response from kwargs
        exception = kwargs.get("exception") # Get exception from kwargs if LiteLLM wrapped it
        
        is_anthropic_model = model and "400" in model.lower() # Check if it's an Anthropic model
        
        print(f"On Async Failure !", isinstance(exception,BadRequestError), "balance is too low" in exception.message)
        
        if isinstance(exception,BadRequestError) and is_anthropic_model and "balance is too low" in exception.message:
            raise RateLimitError(
                message=f"Anthropic model '{model}' returned a 400 Bad Request and 'balance is too low'. Triggering cooldown/fallback.",
                llm_provider="",
                model=model,
                response=raw_response,
            )
        #try:
        #     print(f"On Async Failure !")
        #     print("\nkwargs", kwargs)
        #     # Access kwargs passed to litellm.completion()
        #     model = kwargs.get("model", None)
        #     messages = kwargs.get("messages", None)
        #     user = kwargs.get("user", None)

        #     # Access litellm_params passed to litellm.completion(), example access `metadata`
        #     litellm_params = kwargs.get("litellm_params", {})
        #     metadata = litellm_params.get("metadata", {})   # headers passed to LiteLLM proxy, can be found here

        #     # Access Exceptions & Traceback
        #     exception_event = kwargs.get("exception", None)
        #     traceback_event = kwargs.get("traceback_exception", None)

        #     # Calculate cost using  litellm.completion_cost()
        #     cost = litellm.completion_cost(completion_response=response_obj)
        #     print("now checking response obj")
            
        #     print(
        #         f"""
        #             Model: {model},
        #             Messages: {messages},
        #             User: {user},
        #             Cost: {cost},
        #             Response: {response_obj}
        #             Proxy Metadata: {metadata}
        #             Exception: {exception_event}
        #             Traceback: {traceback_event}
        #         """
        #     )
        # except Exception as e:
        #     print(f"Exception: {e}")

proxy_handler_instance = MyCustomHandler()

# Set litellm.callbacks = [proxy_handler_instance] on the proxy
# need to set litellm.callbacks = [proxy_handler_instance] # on the proxy