using Newtonsoft.Json;
using Newtonsoft.Json;
using RestSharp;
using RestSharp.Authenticators.OAuth2;

namespace Openbanking.Demo
{
    public class AccessTokenClass
    {
        [JsonProperty("access_token")]
        public string AccessToken { get; set; }
    }

    public class AuthPayload
    {
        [JsonProperty("client_id")]
        public string ClientId { get; set; }

        [JsonProperty("client_secret")]
        public string ClientSecret { get; set; }

        [JsonProperty("audience")]
        public string Audience { get; set; }
            
        [JsonProperty("grant_type")]
        public string GrantType { get; set; }
            
        [JsonProperty("scope")]
        public string Scope { get; set; }        

        [JsonProperty("username")]
        public string Username { get; set; }
            
        [JsonProperty("password")]
        public string Password { get; set; }       
    }

    public class OpenbankingApi
    {
        public async Task<AccessTokenClass> LoginAsync()
        {
            //TODO: Refresh token
            var payload = JsonConvert.SerializeObject(new AuthPayload
            {
                ClientId = "<Your client id>",
                ClientSecret = "<Your client secret>",
                Audience = "https://openbankingapi.module",
                GrantType = "password",
                Username = "<your openbanking username>",
                Password = "<your openbanking password>",
                Scope = "email offline_access"
            });
            var client = new RestClient("https://openbanking-iceland.eu.auth0.com");
            var request = new RestRequest("oauth/token", Method.Post)
                .AddJsonBody(payload)
                .AddHeader("content-type", "application/json");
            var response = await client.ExecuteAsync(request);
            return JsonConvert.DeserializeObject<AccessTokenClass>(response.Content);
        }

        private RestClient GetClient(string baseUrl, string token)
        {
            var options = new RestClientOptions(baseUrl)
            {
                ThrowOnAnyError = true,
                MaxTimeout = 10 * 1000
            };

            var client = new RestClient(options);
            client.Authenticator = new OAuth2AuthorizationRequestHeaderAuthenticator(token, "Bearer");
            return client;
        }     

    public async Task<string> GetCurrenty(string companyId, string provider)
    {
        var baseUrl = $"https://{provider}.openbankingapi.is";
        var requestUrl = "/DataPlato/Banks/1.0/currencies/2022-11-03";

        var login = await LoginAsync();
        
        var client = GetClient(baseUrl, login.AccessToken);

        var request = new RestRequest(requestUrl)
            .AddHeader("content-type", "application/json")
            .AddHeader("company-key", companyId)
            .AddHeader("companyId", companyId)
            .AddHeader("appId", "<Your openbanking appid>");
        var response = await client.ExecuteAsync(request);
        return response.Content ?? string.Empty;
    }          
    }

    public class Program
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine("\n------------------------------------------------------------------------------------------");
            var provider = "arionbanki";
            var companyKey = "f745366f-2cab-4ca4-8c67-40dd1dee209f";

            var openbankingApi = new OpenbankingApi();
            var currencies = await openbankingApi.GetCurrenty(companyKey, provider);
            Console.WriteLine(currencies);
        }
    }    
}